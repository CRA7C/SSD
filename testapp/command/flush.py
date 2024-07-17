from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver


class Flush(CommandInterface):
    def __init__(self):
        self.driver = SsdDriver()

    def run(self):
        self.driver.flush()

    @staticmethod
    def is_valid_args(self, *args):
        return True
