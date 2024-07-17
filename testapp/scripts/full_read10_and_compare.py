import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command.__interface import CommandInterface  # noqa E402
from testapp.command import FullRead  # noqa E402


class FullRead10AndCompare(CommandInterface):
    def run(self) -> bool:
        init_data = FullRead().run()
        for _ in range(9):
            test_data = FullRead().run()
            if init_data != test_data:
                return False
        return True


if __name__ == '__main__':
    sys.exit(0 if FullRead10AndCompare().run() else 1)
