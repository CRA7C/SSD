import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command import WriteCommand, ReadCommand  # noqa E402


class Write10AndCompare:
    def run(self) -> bool:
        lba, value = 3, 0x12345678
        for _ in range(10):
            WriteCommand().run(lba, value)
            read_value = ReadCommand().run(lba)
            if value != int(read_value, 16):
                return False
        return True


if __name__ == '__main__':
    sys.exit(0 if Write10AndCompare().run() else 1)
