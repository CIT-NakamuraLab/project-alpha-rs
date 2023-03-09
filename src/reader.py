import os
from time import sleep

import nfc
import dotenv

from logging import getLogger

target_service_code = 0x100b

logger = getLogger(__name__)
dotenv.load_dotenv()


class Reader:
    def __init__(self, flag, array):
        self.flag = flag
        self.array = array

    def on_connect(self, tag):
        idm, pmm = tag.polling(system_code=0x81E1)
        tag.idm, tag.pmm, tag.sys = idm, pmm, 0x81E1

        if isinstance(tag, nfc.tag.tt3.Type3Tag):
            service_code = nfc.tag.tt3.ServiceCode(target_service_code >> 6, target_service_code & 0x3f)
            logger.info(f"Service Code: {service_code}")

            block_code = nfc.tag.tt3.BlockCode(2, service=0)
            logger.info(f"Block Code: {block_code}")

            try:
                raw_data = tag.read_without_encryption([service_code], [block_code])
            except nfc.tag.TagCommandError as e:
                logger.error(e)
            else:
                student_id = raw_data[0:7].decode()
                logger.info(f"Student ID: {student_id}")

                self.flag.set()
                while True:
                    logger.info("Retrieving serial data from Controller...")
                    sleep(0.01)
                    if not self.flag.is_set():
                        logger.info(f"Data Received!: {self.array}")
                        if self.array[7] is 0:
                            logger.warning("Serial Data is invalid!")
                            logger.warning("DATA won't send to Control Server!!")
                            logger.error('Reboot the system.')
                            os.system('systemctl reboot -i')
                            break
                        else:
                            # TODO: POST data to Control Server
                            break

        else:
            logger.error("TAG TYPE ERROR: Tag isn't Type3Tag")
