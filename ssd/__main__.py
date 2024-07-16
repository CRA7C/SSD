import sys

from ssd.ssd import SSD


class SSDRunner:
    def __init__(self):
        self.ssd = SSD()

    def is_valid_command(self):
        return True

    def run(self):
        if sys.argv[1] == 'R':
            self.ssd.read(20)
        elif sys.argv[1] == 'W':
            self.ssd.write(20, '0x1289CDEF')


if __name__ == '__main__':
    runner = SSDRunner()
    if runner.is_valid_command():
        runner.run()
