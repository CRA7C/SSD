import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command import FullReadCommand  # noqa E402


class FullRead10AndCompare:
    def run(self) -> bool:
        init_data = FullReadCommand().run()
        for i, value in enumerate(init_data):
            print(f"LBA: {i:02}, value: {value}")  # print 는 shell 의 출력으로 사용
        print()

        for _ in range(9):
            test_data = FullReadCommand().run()
            for i, value in enumerate(test_data):
                print(f"LBA: {i:02}, value: {value}")  # print 는 shell 의 출력으로 사용
            print()
            if init_data != test_data:
                return False
        return True


if __name__ == '__main__':
    sys.exit(0 if FullRead10AndCompare().run() else 1)
