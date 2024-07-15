from testapp.command.__interface import CommandInterface


class Read(CommandInterface):
    def run(self, *args, **kwarg):
        return '0x12345678'


