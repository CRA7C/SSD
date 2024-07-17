from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver


class Erase(CommandInterface):
    def __init__(self):
        self.driver = SsdDriver()

    def run(self, lba, size):
        self.driver.erase(lba, int(size))
