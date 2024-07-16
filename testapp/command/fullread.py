from testapp.command import Read
from testapp.command.__interface import CommandInterface

START_ADDR = 0
END_ADDR = 99


class FullRead(CommandInterface):
    def __init__(self):
        self.read = Read()

    def run(self, *args, **kwarg):
        self.valid_check(args)

        ret = []
        for addr in range(START_ADDR, END_ADDR + 1):
            ret.append(self.read.run(addr))

        return ret

    def valid_check(self, args):
        if len(args) != 0:
            raise ValueError
