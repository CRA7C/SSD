import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command import FullReadCommand  # noqa E402


class FullReadCompare:
    def run(self) -> bool:
        data1 = FullReadCommand().run()
        for i, value in enumerate(data1):
            print(f"LBA: {i:02}, value: {value}")  # print 는 shell 의 출력으로 사용
        print()

        data2 = FullReadCommand().run()
        for i, value in enumerate(data2):
            print(f"LBA: {i:02}, value: {value}")  # print 는 shell 의 출력으로 사용

        if data1 != data2:
            return False
        return True


if __name__ == '__main__':
    sys.exit(0 if FullReadCompare().run() else 1)
