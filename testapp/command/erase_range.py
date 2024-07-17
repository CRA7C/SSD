from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver

MAXIMUM_ERASE_SIZE_AT_ONCE = 10


class EraseRange(CommandInterface):
    def __init__(self):
        self.driver = SsdDriver()

    def run(self, start_lba: str, end_lba: str):
        size = int(end_lba) - int(start_lba)
        self.driver.erase(int(start_lba), size)
