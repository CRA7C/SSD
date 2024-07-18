import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command import WriteCommand, ReadCommand  # noqa E402

TARGET_LBA = [0, 1, 2, 3, 4, 5]
WRITE_VALUE = 0xAAAABBBB
READ_VALUE = 0x12345678


class TestApp2:
    def __init__(self):
        self.read = ReadCommand()
        self.write = WriteCommand()

    def run(self):
        self.write_30_times()
        self.over_write()
        read_data = self.read_target_lba()
        return all(int(data, 16) == READ_VALUE for data in read_data)

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

    def read_target_lba(self):
        read_data = []
        for lba in TARGET_LBA:
            read_data.append(self.read.run(lba))
        return read_data


if __name__ == '__main__':
    sys.exit(0 if TestApp2().run() else 1)
