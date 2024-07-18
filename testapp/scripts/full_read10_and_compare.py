import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command import FullReadCommand  # noqa E402


class FullRead10AndCompare:
    def run(self) -> bool:
        init_data = FullReadCommand().run()
        for _ in range(9):
            test_data = FullReadCommand().run()
            if init_data != test_data:
                return False
        return True


if __name__ == '__main__':
    sys.exit(0 if FullRead10AndCompare().run() else 1)
