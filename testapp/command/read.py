from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver
from testapp.util import is_in_range_lba


class Read(CommandInterface):
    def __init__(self):
        super().__init__()
        self.driver = SsdDriver()

    def run(self, lba):
        return self.driver.read(lba)

    @staticmethod
    def is_valid_args(self, *args):
        n_lba = args[0]
        return True if is_in_range_lba(n_lba) else False
