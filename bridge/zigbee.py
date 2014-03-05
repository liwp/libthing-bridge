import xbee
from xbee.helpers.dispatch import Dispatch
import serial
    
class ZigBee(object):
    def __init__(self, serial_port, baud_rate, dispatcher, serializer):
        self.ser = serial.Serial(serial_port, baud_rate)
        self.zb = xbee.ZigBee(self.ser)
        self.dispatch = Dispatch(xbee = self.zb)
        self.dispatch.register('rx', self.rx_handler, lambda p: p['id'] == 'rx')
        self.dispatch.register('rx_explicit', self.default_handler, lambda p: p['id'] == 'rx_explicit')
        self.dispatch.register('rx_io_data_long_addr', self.default_handler, lambda p: p['id'] == 'rx_io_data_long_addr')
        self.dispatch.register('tx_status', self.default_handler, lambda p: p['id'] == 'tx_status')
        self.dispatch.register('status', self.default_handler, lambda p: p['id'] == 'status')
        self.dispatch.register('at_response', self.at_response_handler, lambda p: p['id'] == 'at_response')
        self.dispatch.register('remote_at_response', self.default_handler, lambda p: p['id'] == 'remote_at_response')
        self.dispatch.register('node_id_indicator', self.default_handler, lambda p: p['id'] == 'node_id_indicator')
        self.dispatcher = dispatcher
        self.serializer = serializer

    def default_handler(self, name, packet):
        print "%s - %s" % (name, packet)

    def at_response_handler(self, name, packet):
        p = ''.join('%02x' % ord(x) for x in packet['parameter'])
        print "AT - %s = %s" % (packet['command'], p)

    def rx_handler(self, name, packet):
        req = self.serializer.deserialize_request(packet['rf_data'])
        if not req:
            print "Ignoring garbage request"
            return
        
        rsp = self.dispatcher.dispatch(req)
        data = self.serializer.serialize_response(rsp)
        dst_long = packet['source_addr_long']
        dst_addr = packet['source_addr']
        self.zb.tx(dest_addr_long=dst_long, dest_addr=dst_addr, data=data)

    def run(self):
        try:
            print "Run!"
            self.dispatch.run()
        except KeyboardInterrupt:
            pass

        print "Bye!"
        self.ser.close()
