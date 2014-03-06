import zigbee
import books
import tags
import dispatcher
import serializer
import os

def main():
    serial_port = os.getenv('LIBTHING_PORT', '/dev/ttyAMA0')
    baud_rate = 9600
    
    #id_service = tags.DummyTags()
    id_service = tags.DeploydTags('http://10.120.200.158:2403/users')
    lib_service = books.DummyBooks()
    #lib_service = books.DeploydBooks('http://localhost:2404/books')
    disp = dispatcher.Dispatcher(id_service, lib_service)
    ser = serializer.Serializer()
    serial = zigbee.ZigBee(serial_port, baud_rate, disp, ser)
    serial.run()

if __name__ == '__main__':
    main()
