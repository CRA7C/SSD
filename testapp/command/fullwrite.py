from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver
from testapp.constants import SSD_LBA_RANGE
from testapp.util import validate_ssd_value, is_valid_hex


class FullWrite(CommandInterface):
    def __init__(self):
        super().__init__()
        self.driver = SsdDriver()

    def run(self, value):
        for i in SSD_LBA_RANGE:
            self.driver.write(i, value)

    @staticmethod
    def is_valid_args(self, *args):
        value = args[0]
        return True if is_valid_hex(value) else False
