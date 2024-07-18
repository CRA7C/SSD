import sys
from pathlib import Path
from random import randint

sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command import WriteCommand, ReadCommand, EraseCommand  # noqa E402


class WriteAndErase:
    def run(self) -> bool:
        lba, value = randint(0, 99), randint(1, 0xFFFFFFFF)
        WriteCommand().run(lba, value)
        EraseCommand().run(lba, 2)
        ret = ReadCommand().run(lba)
        return ret == "0x00000000"


if __name__ == '__main__':
    sys.exit(0 if WriteAndErase().run() else 1)
