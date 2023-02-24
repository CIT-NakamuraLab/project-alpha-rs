import asyncio
from concurrent.futures import ProcessPoolExecutor

import nfc

import time
from logging import basicConfig, getLogger, DEBUG

from src.controller import serial_init, serial_read
from reader import on_connect

basicConfig(level=DEBUG)
logger = getLogger(__name__)


def start_nfc_reader():
    while True:
        with nfc.ContactlessFrontend('usb') as reader:
            logger.info("NFC Reader is READY")
            try:
                reader.connect(rdwr={'on-connect': on_connect})
                time.sleep(1)
            except nfc.tag.tt3.Type3TagCommandError as exception:
                logger.error("READ ERROR, Try again", exception)


def start_controller():
    serial_port = serial_init()
    try:
        asyncio.run(serial_read(serial_port))
    except KeyboardInterrupt:
        serial_port.close()


def main():
    with ProcessPoolExecutor() as executor:
        executor.submit(start_nfc_reader)
        executor.submit(start_controller)


if __name__ == "__main__":
    main()

