import sys

from testapp.command.__interface import CommandInterface


class Exit(CommandInterface):
    def run(self, *args, **kwarg):
        sys.exit()
