from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver
from testapp.constants import SSD_SIZE


class FullWrite(CommandInterface):
    def __init__(self):
        super().__init__()
        self.driver = SsdDriver()

    def run(self, value):
        for i in range(SSD_SIZE):
            self.driver.write(i, value)
