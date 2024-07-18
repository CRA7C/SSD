import sys
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command.__interface import CommandInterface  # noqa E402
from testapp.command import Write, Read  # noqa E402

TARGET_LBA = [0, 1, 2, 3, 4, 5]
WRITE_VALUE = 0xAAAABBBB
READ_VALUE = 0x12345678


class TestApp2(CommandInterface):
    def __init__(self):
        self.read = Read()
        self.write = Write()

    def run(self) -> bool:
        self.write_30_times()
        self.over_write()
        read_data = self.read_target_lba()
        return self.validate(read_data)

    def write_30_times(self):
        # Total 30회의 write을 수행.
        call_count = 0
        while call_count < 30:
            for lba in TARGET_LBA:
                self.write.run(lba, WRITE_VALUE)
                call_count += 1

    def over_write(self):
        for lba in TARGET_LBA:
            self.write.run(lba, READ_VALUE)

    def read_target_lba(self) -> List[str]:
        read_data = []
        for lba in TARGET_LBA:
            read_data.append(self.read.run(lba))
        return read_data

    @staticmethod
    def validate(read_data: List[str]) -> bool:
        for data in read_data:
            if int(data, 16) != READ_VALUE:
                return False
        return True

    @staticmethod
    def is_valid_args(self, *args):
        return True


if __name__ == '__main__':
    sys.exit(0 if TestApp2().run() else 1)
