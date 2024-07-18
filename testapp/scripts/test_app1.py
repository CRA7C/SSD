import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command import FullReadCommand, FullWriteCommand  # noqa E402

READ_VALUE = 0x12345678


class TestApp1:

    def run(self):
        FullWriteCommand().run(READ_VALUE)
        read_data = FullReadCommand().run()
        is_valid = all(int(data, 16) == READ_VALUE for data in read_data)

        if is_valid:
            for i, value in enumerate(read_data):
                print(f"LBA: {i:02}, value: {value}")  # print 는 shell 의 출력으로 사용

        return is_valid


if __name__ == '__main__':
    sys.exit(0 if TestApp1().run() else 1)
