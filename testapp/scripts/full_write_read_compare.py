import sys
from pathlib import Path
from random import randint
sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command import FullReadCommand, FullWriteCommand  # noqa E402
from testapp.constants import SSD_MIN_VALUE, SSD_MAX_VALUE  # noqa E402


class FullWriteReadCompare:
    def run(self) -> bool:
        value = randint(SSD_MIN_VALUE, SSD_MAX_VALUE)
        FullWriteCommand().run(value)
        read_data = FullReadCommand().run()
        return all(int(data, 16) == value for data in read_data)

    @staticmethod
    def is_valid_args(*args):
        return True


if __name__ == '__main__':
    sys.exit(0 if FullWriteReadCompare().run() else 1)
