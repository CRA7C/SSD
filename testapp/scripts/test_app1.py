import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))  # testapp 접근을 위함
from testapp.command.__interface import CommandInterface  # noqa E402
from testapp.command import FullRead, FullWrite  # noqa E402
from testapp.constants import SSD_MIN_VALUE, SSD_MAX_VALUE  # noqa E402

READ_VALUE = 0x12345678


class TestApp1(CommandInterface):

    def run(self):
        FullWrite().run(READ_VALUE)
        read_data = FullRead().run()
        return self.validate_data(read_data)

    @staticmethod
    def validate_data(read_data):
        for data in read_data:
            if int(data, 16) != READ_VALUE:
                return False
        return True

    @staticmethod
    def is_valid_args(self, *args):
        return True


if __name__ == '__main__':
    sys.exit(0 if TestApp1().run() else 1)
