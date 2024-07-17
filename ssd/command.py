class Command:
    def __init__(self, args):
        self.option = args[0]
        self.args = args

    def get_value(self):
        return self.args


class ReadCommand(Command):
    def __init__(self, args):
        super().__init__(args)
        self.lba = int(args[1])


class WriteCommand(Command):
    def __init__(self, args):
        super().__init__(args)
        self.lba = int(args[1])
        self.value = int(args[2], 16)

    def get_key(self):
        return (self.option, self.lba, self.lba + 1)


class EraseCommand(Command):
    def __init__(self, args):
        super().__init__(args)
        self.lba = int(args[1])
        self.size = int(args[2])

    def get_key(self):
        return (self.option, self.lba, self.lba + self.size)


class CommandFactory:
    @staticmethod
    def parse_command(command_list):
        name = command_list[0]
        if name == 'R':
            return ReadCommand(command_list)
        elif name == 'W':
            return WriteCommand(command_list)
        elif name == 'E':
            return EraseCommand(command_list)
        else:
            return Command(command_list)
