import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command import FullReadCommand  # noqa E402


class FullReadCompare:
    def run(self) -> bool:
        data1 = FullReadCommand().run()
        data2 = FullReadCommand().run()
        if data1 != data2:
            return False
        return True

    @staticmethod
    def is_valid_args(*args, **kwarg):
        return True


if __name__ == '__main__':
    sys.exit(0 if FullReadCompare().run() else 1)
