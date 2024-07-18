import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[2].resolve()))


class DummyTest:
    def run(self) -> bool:
        return True


if __name__ == '__main__':
    sys.exit(0 if DummyTest().run() else 1)
