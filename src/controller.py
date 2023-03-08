import sys
import serial
import time
from serial import SerialException

from logging import getLogger

logger = getLogger(__name__)

def serial_init():
    com = '/dev/ttyACM0'
    baudrate = 115200
    try:
        serial_port = serial.Serial(com, baudrate)
        logger.info(f"{com} OPEN.")
    except SerialException:
        logger.error(f"Cannot open {com}.")
        sys.exit(-1)
    return serial_port


def serial_read(serial_port):
    try:
        # どんな理由であれ、5回データ取得に失敗したらエラーを返します。
        for try_count in range(5):

            # ゴミ防止
            serial_port.read(serial_port.inWaiting())

            # 1バイトデータを送信してデータ要求。'a'に意味は無い。
            serial_port.write(b'a')
            # 0.1秒待ちます。返答が来なければリトライします。
            for i in range(10):
                if serial_port.inWaiting() >= 3:
                    break
                time.sleep(0.01)
            else:
                continue

            # シリアルポートのバッファを読み込みます。
            # ヘッダっぽい物があったら次に進みます。
            for i in range(serial_port.inWaiting()):
                if b'\x00' == serial_port.read():
                    break
            else:
                continue

            data = int.from_bytes(serial_port.read(), 'big')
            data_check = int.from_bytes(serial_port.read(), 'big')

            # データチェック
            if data & 0xff != ~data_check & 0xff:
                continue

            out = []
            for i in range(8):
                out.append((data >> i) % 2)

            return True, out

        else:
            logger.warning("Failed to get button/key data.")
            return False, []

    except KeyboardInterrupt:
        serial_port.close()
        return False, []
