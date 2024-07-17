from ssd.common import convert_hex_to_str
from ssd.nand_driver import NandDriver
from ssd.result_manager import ResultManager


class SolidStateDrive:
    def __init__(self):
        self.nand_driver = NandDriver()
        self.result_manager = ResultManager()

    def write(self, lba: int, value):
        self.nand_driver.write(lba, value)

    def read(self, lba: int):
        result = self.nand_driver.read(lba)
        self.result_manager.write(convert_hex_to_str(result))

    def read_fast(self, value):
        self.result_manager.write(convert_hex_to_str(value))

    def erase(self, lba: int, n_value: int):
        self.nand_driver.erase(lba, n_value)
