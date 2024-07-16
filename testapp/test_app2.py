"""
TestApp2 제작하기
 • 0 ~ 5 번 LBA 에 0xAAAABBBB 값으로 총 30번 Write를 수행한다.
 • 0 ~ 5 번 LBA 에 0x12345678 값으로 1 회 Over Write를 수행한다.
 • 0 ~ 5 번 LBA Read 했을 때 정상적으로 값이 읽히는지 확인한다
"""
from testapp.command import Write, Read
from testapp.command.__interface import CommandInterface

WRITE_VALUE = 0xAAAABBBB


class TestApp2(CommandInterface):
    def run(self, *args, **kwargs):
        self.write_30_times()
        self.over_write()

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
                write.run(lba, 0x12345678)
        except Exception:
            raise Exception
        return True
