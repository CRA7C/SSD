import sys
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command.__interface import CommandInterface  # noqa E402
from testapp.command import FullRead, FullWrite  # noqa E402

READ_VALUE = 0x12345678


class TestApp1(CommandInterface):

    def run(self) -> bool:
        FullWrite().run(READ_VALUE)
        read_data = FullRead().run()
        return self.validate_data(read_data)

    @staticmethod
    def validate_data(read_data: List[str]) -> bool:
        for data in read_data:
            if int(data, 16) != READ_VALUE:
                return False
        return True

    @staticmethod
    def is_valid_args(self, *args):
        return True


if __name__ == '__main__':
    sys.exit(0 if TestApp1().run() else 1)
