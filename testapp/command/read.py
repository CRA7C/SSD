from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver


class Read(CommandInterface):
    def __init__(self):
        super().__init__()
        self.driver = SsdDriver()

    def run(self, lba):
        return self.driver.read(lba)
