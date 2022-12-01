import nfc

import time
from logging import basicConfig, getLogger, DEBUG, INFO

basicConfig(level=DEBUG)
logger = getLogger(__name__)

target_service_code = 0x100b


def connected(tag):
    idm, pmm = tag.polling(system_code=0x81E1)
    tag.idm, tag.pmm, tag.sys = idm, pmm, 0x81E1

    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        service_code = nfc.tag.tt3.ServiceCode(target_service_code >> 6, target_service_code & 0x3f)
        logger.debug(f"Service Code: {service_code}")

        block_code = nfc.tag.tt3.BlockCode(2, service=0)
        logger.debug(f"Block Code: {block_code}")

        try:
            raw_data = tag.read_without_encryption([service_code], [block_code])
        except nfc.tag.TagCommandError as e:
            logger.error(e)
        else:
            student_id = raw_data[0:7].decode()
            logger.info(f"Student ID: {student_id}")

    else:
        logger.info("TAG TYPE ERROR: Tag isn't Type3Tag")


def main():
    while True:
        with nfc.ContactlessFrontend('usb') as reader:
            logger.info("NFC Reader is READY")
            try:
                reader.connect(rdwr={'on-connect': connected})
                time.sleep(1)
            except nfc.tag.tt3.Type3TagCommandError as exception:
                logger.error("READ ERROR, Try again", exception)


if __name__ == "__main__":
    main()