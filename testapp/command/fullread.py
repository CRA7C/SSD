from testapp.command import Read
from testapp.command.__interface import CommandInterface

STARTADDR = 0
ENDADDR = 99


class FullRead(CommandInterface):
    def __init__(self):
        self.read = Read()

    def run(self, *args, **kwarg):
        self.valid_check(args)

        for addr in range(STARTADDR, ENDADDR + 1):
            print(self.read.run(addr))

    def valid_check(self, args):
        if len(args) != 0:
            raise ValueError
