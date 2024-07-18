import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command import FullReadCommand, FullWriteCommand  # noqa E402

READ_VALUE = 0x12345678


class TestApp1:

    def run(self):
        FullWriteCommand().run(READ_VALUE)
        read_data = FullReadCommand().run()
        return all(int(data, 16) == READ_VALUE for data in read_data)


if __name__ == '__main__':
    sys.exit(0 if TestApp1().run() else 1)
