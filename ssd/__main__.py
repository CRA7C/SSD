import sys

from ssd.solidstatedrive import SolidStateDrive
from ssd.common import LBA_LOWER_LIMIT, LBA_UPPER_LIMIT


class SSDRunner:
    def __init__(self):
        self.ssd = SolidStateDrive()

    @staticmethod
    def is_valid_command():
        if len(sys.argv) < 3:
            raise ValueError("명령을 수행하기 위한 인자가 부족합니다. ex) ssd R 20/ssd W 20 0x1289CDEF")

        if sys.argv[1] not in ('R', 'W'):
            raise ValueError('R 또는 W를 사용해주세요.(대문자)')

        if not LBA_LOWER_LIMIT <= int(sys.argv[2]) <= LBA_UPPER_LIMIT:
            raise ValueError(f'LBA는 {LBA_LOWER_LIMIT} ~ {LBA_UPPER_LIMIT} 여야합니다.')

        if sys.argv[1] == 'W':
            if len(sys.argv) < 4:
                raise ValueError('W 명령에는 value가 필요합니다.')
            if len(sys.argv[3]) != 10 or sys.argv[3][:2] != '0x':
                raise ValueError('value는 0x00000000 형식이여야 합니다.')
            int(sys.argv[3], 16)
        return True

    def run(self):
        lba = int(sys.argv[2])
        if sys.argv[1] == 'R':
            self.ssd.read(lba)
        elif sys.argv[1] == 'W':
            value = int(sys.argv[3][2:], 16)
            self.ssd.write(lba, value)


if __name__ == '__main__':
    runner = SSDRunner()
    if runner.is_valid_command():
        runner.run()
