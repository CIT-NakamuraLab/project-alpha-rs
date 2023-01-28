import sys

import serial
from serial import SerialException

raw_text = ""
inte = ""
deci = ""


def serial_init():
    try:
        serial_port = serial.Serial("COM8", 115200)
        print('OPEN COM8')
    except SerialException:
        print("シリアルポートを開けません。")
        sys.exit(-1)
    return serial_port


def serial_read(serial_port):
    global raw_text, inte, deci
    try:
        while True:
            raw_text = serial_port.readline().decode('utf8').replace('\r', '').replace('\n', '')
            inte, deci = raw_text.split('.')
    except KeyboardInterrupt:
        serial_port.close()
