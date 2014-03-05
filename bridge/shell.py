import sys, time, cmd, serial, binascii, os, struct
from xbee import ZigBee

LIBTHING_PORT = os.getenv('LIBTHING_PORT', '/dev/tty.usbserial-A1011HQ7')
HUB_ADDR = struct.pack('>Q', 0) # 64-bit 0s
BCAST_ADDR = '\xFF\xFE'

class LibThingShell(cmd.Cmd):
    intro = "Welcome to the LibThing/XBee shell. Type help or ? to list commands.\n"
    prompt = "xbee% "
    file = None
    serial = serial.Serial(LIBTHING_PORT, 9600)
    zigbee = ZigBee(serial)

    def do_id(self, p):
        self.at_command('ID')
        self.at_command('SH')
        self.at_command('SL')
        self.at_command('MY')

    def do_at(self, cmd):
        self.at_command(cmd)
        
    def at_command(self, cmd):
        self.zigbee.send('at', command=cmd)
        packet = self.zigbee.wait_read_frame()
        p = ''.join('%02x' % ord(x) for x in packet['parameter'])
        print "AT - %s = %s" % (packet['command'], p)

    def do_tag(self, arg):
        args = parse(arg)
        tag = int(args[0], 16)
        print tag
        print type(tag)
        data = struct.pack('<cL', 'T', tag)
        self.send(data)
        self.recv()

    def do_book(self, arg):
        args = parse(arg)
        isbn = args[0]
        data = struct.pack('<c128p', 'B', isbn)
        self.send(data)
        self.recv()

    def do_lend(self, arg):
        args = parse(arg)
        print args
        tag = args[0].decode('hex')
        isbn = args[1]
        data = struct.pack('<cL128p', 'L', tag, isbn)
        self.send(data)
        self.recv()

    def do_EOF(self, p):
        return self.do_exit(p)
        
    def do_exit(self, p):
        """Exits from the XBee serial console"""
        self.serial.close()
        return 1
    
    def send(self, data):
        self.zigbee.tx(dest_addr_long=HUB_ADDR, dest_addr=BCAST_ADDR, data=data)

    def recv(self):
        packet = self.zigbee.wait_read_frame()
        tx_ok = packet['deliver_status'] == '\x00'
        if tx_ok:
            print "TX status - OK"
        else:
            print "TX status - FAIL - %s" % packet
            
        packet = self.zigbee.wait_read_frame()
        data = packet['rf_data']
        code = data[0]
        {'T': self.recv_tag,
         'B': self.recv_book,
         'L': self.recv_lend}[code](data[1:])
         
    def recv_tag(self, data):
        print data
        id = struct.unpack('<128p', data)[0]
        if len(id) == 0:
            print "RX - unknown user"
        else:
            print "RX - user: %s" % id
         
    def recv_book(self, data):
        title = struct.unpack('<128p', data)[0]
        if len(title) == 0:
            print "RX - book does not exist"
        else:
            print "RX - book: %s" % title
         
    def recv_lend(self, data):
        status = struct.unpack('<c', data)[0]
        if status == 'B':
            print "RX - book borrowed"
        elif status == 'R':
            print "RX - book returned"
        elif status == 'F':
            print "RX - failure"
        else:
            print "RX - unknown status code: %s" % status
        
def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(arg.split())

if __name__ == '__main__':
	shell = LibThingShell()
	shell.cmdloop()
