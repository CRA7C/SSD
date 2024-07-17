from testapp.command.__interface import CommandInterface
from testapp.command.erase_common import request_erase
from testapp.constants import SSD_SIZE
from testapp.ssd_driver import SsdDriver
from testapp.util import is_valid_size, is_in_range_lba


class Erase(CommandInterface):
    def __init__(self):
        self.driver = SsdDriver()

    def run(self, lba: str, total_size: str):
        erase_size = int(total_size)
        initial_lba = int(lba)
        target_lba = initial_lba + erase_size
        end_lba = SSD_SIZE if target_lba > SSD_SIZE else target_lba
        request_erase(self.driver, initial_lba, end_lba)

    @staticmethod
    def is_valid_args(self, *args):
        n_lba = args[0]
        size = args[1]
        if not is_in_range_lba(n_lba):
            return False
        if not is_valid_size(size):
            return False
        return True
