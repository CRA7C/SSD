class AppSSD:
    def __init__(self):
        self.nand_driver = None
        self.result_manager = None
        pass

    def read(self, lba) -> int:
        pass

    def write(self, lba, value):
        pass

    def exit(self):
        pass

    def help(self):
        pass

    def fullwrite(self, value):  # noqa
        pass

    def fullread(self):  # noqa
        pass

    def parse_command(self, cmd):
        pass
