import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command.__interface import CommandInterface  # noqa E402
from testapp.command import Write, Read  # noqa E402


class Write10AndCompare(CommandInterface):
    def run(self) -> bool:
        lba, value = 3, 0x12345678
        for _ in range(10):
            Write().run(lba, value)
            read_value = Read().run(lba)
            if value != int(read_value, 16):
                return False
        return True

    @staticmethod
    def is_valid_args(self, *args):
        return True


if __name__ == '__main__':
    sys.exit(0 if Write10AndCompare().run() else 1)
