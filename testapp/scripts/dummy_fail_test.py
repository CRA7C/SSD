import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2].resolve()))


class DummyFailTest:
    def run(self) -> bool:
        return False


if __name__ == '__main__':
    sys.exit(0 if DummyFailTest().run() else 1)
