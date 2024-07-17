from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver
from testapp.util import is_in_range_lba, is_valid_hex


class Write(CommandInterface):
    def __init__(self):
        super().__init__()
        self.driver = SsdDriver()

    def run(self, lba, value):
        self.driver.write(lba, value)

    @staticmethod
    def is_valid_args(self, *args):
        n_lba = args[0]
        value = args[1]
        if not is_in_range_lba(n_lba):
            return False
        if not is_valid_hex(value):
            return False
        return True
