from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver
from testapp.util import get_ssd_result


class Read(CommandInterface):
    def __init__(self):
        self.driver = SsdDriver()

    def run(self, lba):
        self.driver.read(lba)

        return get_ssd_result()
