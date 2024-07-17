"""
TestApp1 제작하기
 • Test Shell 에서 “testapp1” 명령어를 입력하면 Script가 수행된다.
 • 먼저 fullwrite를 수행한다.
 • fullread를 하면서, write 한 값대로 read가 되는지 확인한다.
   🡪 SSD가 정상 동작하는지 확인하는 테스트 스크립트
"""
from testapp.command.__interface import CommandInterface
from testapp.command import FullRead, FullWrite

READ_VALUE = 0x12345678


class TestApp1(CommandInterface):

    def run(self, *args, **kwargs):
        FullWrite().run(READ_VALUE)
        read_data = FullRead().run()
        return self.validate_data(read_data)

    @staticmethod
    def validate_data(read_data):
        for data in read_data:
            if int(data, 16) != READ_VALUE:
                return False
        return True
