import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))  # testapp 접근을 위함
from testapp.command.__interface import CommandInterface  # noqa E402
from testapp.command import FullRead  # noqa E402
from testapp.constants import SSD_MIN_VALUE, SSD_MAX_VALUE  # noqa E402


class FullRead10AndCompare(CommandInterface):
    def run(self) -> bool:
        init_data = FullRead().run()
        for _ in range(9):
            test_data = FullRead().run()
            if init_data != test_data:
                return False
        return True


if __name__ == '__main__':
    sys.exit(0 if FullRead10AndCompare().run() else 1)
