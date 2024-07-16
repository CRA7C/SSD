import sys

from ssd.ssd import SSD


class SSDRunner:
    def __init__(self):
        self.ssd = SSD()

    def is_valid_command(self):
        if len(sys.argv) < 2:
            raise TypeError
        return True

    def run(self):
        lba = int(sys.argv[2])
        if sys.argv[1] == 'R':
            self.ssd.read(lba)
        elif sys.argv[1] == 'W':
            value = int(sys.argv[3][2:], 16)
            self.ssd.write(lba, value)


if __name__ == '__main__':
    runner = SSDRunner()
    if runner.is_valid_command():
        runner.run()
