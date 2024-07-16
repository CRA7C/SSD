"""
TestApp2 제작하기
 • 0 ~ 5 번 LBA 에 0xAAAABBBB 값으로 총 30번 Write를 수행한다.
 • 0 ~ 5 번 LBA 에 0x12345678 값으로 1 회 Over Write를 수행한다.
 • 0 ~ 5 번 LBA Read 했을 때 정상적으로 값이 읽히는지 확인한다
"""
from testapp.command import Write, Read
from testapp.command.__interface import CommandInterface

WRITE_VALUE = 0xAAAABBBB
READ_VALUE = 0x12345678


class TestApp2(CommandInterface):
    def run(self, *args, **kwargs):
        self.write_30_times()
        self.over_write()
        read_data = self.read()
        return self.validate(read_data)

    def write_30_times(self):
        write = Write()
        try:
            for _ in range(6):
                for lba in range(5):
                    write.run(lba, WRITE_VALUE)
        except Exception:
            raise Exception
        return True

    def over_write(self):
        write = Write()
        try:
            for lba in range(6):
                write.run(lba, READ_VALUE)
        except Exception:
            raise Exception
        return True

    def read(self):
        read = Read()
        read_data = []
        for lba in range(6):
            read_data.append(read.run(lba))
        return read_data

    def validate(self, read_data):
        for data in read_data:
            if data != READ_VALUE:
                return False
        return True

