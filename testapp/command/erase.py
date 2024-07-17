from testapp.command.__interface import CommandInterface
from testapp.command.erase_common import request_erase
from testapp.constants import SSD_SIZE
from testapp.ssd_driver import SsdDriver


class Erase(CommandInterface):
    def __init__(self):
        self.driver = SsdDriver()

    def run(self, lba: str, total_size: str):
        erase_size = int(total_size)
        initial_lba = int(lba)
        target_lba = initial_lba + erase_size
        end_lba = SSD_SIZE if target_lba > SSD_SIZE else target_lba
        request_erase(self.driver, initial_lba, end_lba)
