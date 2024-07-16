"""
TestApp2 제작하기
 • 0 ~ 5 번 LBA 에 0xAAAABBBB 값으로 총 30번 Write를 수행한다.
 • 0 ~ 5 번 LBA 에 0x12345678 값으로 1 회 Over Write를 수행한다.
 • 0 ~ 5 번 LBA Read 했을 때 정상적으로 값이 읽히는지 확인한다
"""
from testapp.command import Write, Read
from testapp.command.__interface import CommandInterface

TARGET_LBA = [0, 1, 2, 3, 4, 5]
WRITE_VALUE = 0xAAAABBBB
READ_VALUE = 0x12345678


class TestApp2(CommandInterface):
    def __init__(self):
        self.read = Read()
        self.write = Write()

    def run(self, *args, **kwargs):
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

    def read_target_lba(self):
        read_data = []
        for lba in TARGET_LBA:
            read_data.append(self.read.run(lba))
        return read_data

    @staticmethod
    def validate(read_data):
        for data in read_data:
            if data != READ_VALUE:
                return False
        return True
