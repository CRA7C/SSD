import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2].resolve()))
from testapp.command.__interface import CommandInterface  # noqa E402


class DummyTest(CommandInterface):
    def run(self) -> bool:
        return True

    @staticmethod
    def is_valid_args(self, *args):
        return True


if __name__ == '__main__':
    sys.exit(0 if DummyTest().run() else 1)
