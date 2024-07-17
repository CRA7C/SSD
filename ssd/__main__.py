import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ssd.solidstatedrive import SolidStateDrive
from ssd.common import LBA_LOWER_LIMIT, LBA_UPPER_LIMIT, is_valid_hex


class SSDRunner:
    def __init__(self):
        self.ssd = SolidStateDrive()

    @staticmethod
    def is_valid_command():
        if len(sys.argv) < 3:
            raise ValueError("명령을 수행하기 위한 인자가 부족합니다. ex) ssd R 20/ssd W 20 0x1289CDEF/ssd E 10 3")

        if sys.argv[1] not in ('R', 'W', 'E'):
            raise ValueError('R, W, E 중 하나를 사용해주세요.(대문자)')

        if not sys.argv[2].isdigit():
            raise ValueError('LBA는 숫자여야합니다.')

        if not LBA_LOWER_LIMIT <= int(sys.argv[2]) <= LBA_UPPER_LIMIT:
            raise ValueError(f'LBA는 {LBA_LOWER_LIMIT} ~ {LBA_UPPER_LIMIT} 여야합니다.')

        if sys.argv[1] == 'W':
            if len(sys.argv) < 4:
                raise ValueError('W 명령에는 value가 필요합니다.')
            if not is_valid_hex(sys.argv[3]):
                raise ValueError('value는 0x00000000 형식이여야 합니다.')
        if sys.argv[1] == 'E':
            if len(sys.argv) < 4:
                raise ValueError('E 명령에는 시작 LBA, 지울 데이터 갯수가 필요합니다.')
            if not sys.argv[3].isdigit():
                raise ValueError('지울 데이터 갯수는 숫자여야합니다.')
            if not 1 <= int(sys.argv[3]) <= 10:
                raise ValueError('지울 데이터 갯수는 1이상 10이하만 가능합니다.')
        return True

    def run(self):
        lba = int(sys.argv[2])
        if sys.argv[1] == 'R':
            self.ssd.read(lba)
        elif sys.argv[1] == 'W':
            value = int(sys.argv[3], 16)
            self.ssd.write(lba, value)
        elif sys.argv[1] == 'E':
            n_value = int(sys.argv[3])
            self.ssd.erase(lba, n_value)


if __name__ == '__main__':
    runner = SSDRunner()
    if runner.is_valid_command():
        runner.run()
