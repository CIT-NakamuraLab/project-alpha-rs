from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager

import nfc

import time
from logging import basicConfig, getLogger, DEBUG

from src.controller import serial_init, serial_read
from reader import Reader

basicConfig(level=DEBUG)
logger = getLogger(__name__)


def start_nfc_reader(flag, shared_array):
    card_reader = Reader(flag, shared_array)
    while True:
        with nfc.ContactlessFrontend('usb') as reader:
            logger.info("NFC Reader is READY")
            try:
                reader.connect(rdwr={'on-connect': card_reader.on_connect})
                time.sleep(1)
            except nfc.tag.tt3.Type3TagCommandError as exception:
                logger.error("READ ERROR, Try again", exception)


def start_controller(flag, shared_array):
    serial_port = serial_init()
    while True:
        if flag.is_set():
            try:
                result = serial_read(serial_port)
                if result[0]:
                    # Sets the value read against the shared array on a successful serial read.
                    for i, item in enumerate(result[1]):
                        shared_array[i] = result[1][i]
                    # The flag is released and the reader is notified that the value has been set.
                    flag.clear()
                else:
                    continue
            except KeyboardInterrupt:
                serial_port.close()


def main():
    manager = Manager()
    flag = manager.Event()
    shared_array = manager.Array('i', [0, 0, 0, 0, 0, 0, 0, 0])

    with ProcessPoolExecutor() as executor:
        executor.submit(start_nfc_reader, flag, shared_array)
        executor.submit(start_controller, flag, shared_array)


if __name__ == "__main__":
    main()

