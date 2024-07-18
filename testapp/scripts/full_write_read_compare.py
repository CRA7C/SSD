import sys
from pathlib import Path
from random import randint

sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command.__interface import CommandInterface  # noqa E402
from testapp.command import FullRead, FullWrite  # noqa E402
from testapp.constants import SSD_MIN_VALUE, SSD_MAX_VALUE  # noqa E402


class FullWriteReadCompare(CommandInterface):
    def run(self) -> bool:
        value = randint(SSD_MIN_VALUE, SSD_MAX_VALUE)
        FullWrite().run(value)
        read_data = FullRead().run()
        return all(int(data, 16) == value for data in read_data)

    @staticmethod
    def is_valid_args(self, *args):
        return True


if __name__ == '__main__':
    sys.exit(0 if FullWriteReadCompare().run() else 1)
