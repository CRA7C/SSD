"""
TestApp1 제작하기
 • Test Shell 에서 “testapp1” 명령어를 입력하면 Script가 수행된다.
 • 먼저fullwrite를 수행한다.
 • fullread를 하면서, write 한 값대로 read가 되는지 확인한다.
   🡪 SSD가 정상동작하는지확인하는테스트스크립트
"""
from testapp.command.__interface import CommandInterface
from testapp.command import FullRead, FullWrite


class TestApp1(CommandInterface):

    def run(self, *args, **kwargs):
        FullWrite().run(0x12345678)
        read_data = FullRead().run()
        return self.validate_data(read_data)

    def validate_data(self, read_data):
        for data in read_data:
            if data != 0x12345678:
                return False
        return True
