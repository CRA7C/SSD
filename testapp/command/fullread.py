from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver
from testapp.constants import SSD_LBA_RANGE


class FullRead(CommandInterface):
    def __init__(self):
        super().__init__()
        self.driver = SsdDriver()

    def run(self):
        return [self.driver.read(addr) for addr in SSD_LBA_RANGE]

    @staticmethod
    def is_valid_args(self, *args):
        return True
