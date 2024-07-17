from testapp.command.__interface import CommandInterface
from testapp.command.erase_common import request_erase
from testapp.ssd_driver import SsdDriver
from testapp.util import is_in_range_lba


class EraseRange(CommandInterface):
    def __init__(self):
        self.driver = SsdDriver()

    def run(self, start_lba: str, end_lba: str):
        request_erase(self.driver, int(start_lba), int(end_lba))

    @staticmethod
    def is_valid_args(self, *args):
        start_lba = args[0]
        end_lba = args[1]
        if not (is_in_range_lba(start_lba) and is_in_range_lba(end_lba)):
            return False
        if int(start_lba) >= int(end_lba):
            return False
        return True
