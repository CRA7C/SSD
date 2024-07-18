import sys
from pathlib import Path
from random import randint

sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command.__interface import CommandInterface  # noqa E402
from testapp.command import Write, Read  # noqa E402
from testapp.constants import (SSD_START_LBA, SSD_END_LBA,
                               SSD_MAX_VALUE, SSD_MIN_VALUE)  # noqa E402


class Loop_WriteAndReadCompare(CommandInterface):  # noqa
    def run(self) -> bool:
        for _ in range(10):
            lba, value = randint(SSD_START_LBA, SSD_END_LBA), randint(SSD_MIN_VALUE, SSD_MAX_VALUE)
            Write().run(lba, value)
            read_value = Read().run(lba)
            if value != int(read_value, 16):
                return False
        return True

    @staticmethod
    def is_valid_args(self, *args):
        return True


if __name__ == '__main__':
    sys.exit(0 if Loop_WriteAndReadCompare().run() else 1)
