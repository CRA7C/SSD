from ssd.nand_driver import NandDriver
from ssd.result_manager import ResultManager


class SSD:
    def __init__(self):
        self.nand_driver = NandDriver()
        self.result_manager = ResultManager()

    def write(self, lba, value):
        self.nand_driver.write(lba, value)

    def read(self, lba):
        self.result_manager.write(self.nand_driver.read(lba))
