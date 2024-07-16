"""
TestApp2 제작하기
 • 0 ~ 5 번 LBA 에 0xAAAABBBB 값으로 총 30번 Write를 수행한다.
 • 0 ~ 5 번 LBA 에 0x12345678 값으로 1 회 Over Write를 수행한다.
 • 0 ~ 5 번 LBA Read 했을 때 정상적으로 값이 읽히는지 확인한다
"""
from testapp.command.__interface import CommandInterface


class TestApp2(CommandInterface):
    def run(self, *args, **kwargs):
        pass
