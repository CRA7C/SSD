from testapp.command.__interface import CommandInterface
from testapp.command.erase_common import request_erase
from testapp.ssd_driver import SsdDriver


class EraseRange(CommandInterface):
    def __init__(self):
        self.driver = SsdDriver()

    def run(self, start_lba: str, end_lba: str):
        request_erase(self.driver, int(start_lba), int(end_lba))
