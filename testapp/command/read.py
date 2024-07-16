from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver
from testapp.util import get_ssd_result


class Read(CommandInterface):
    def __init__(self):
        self.driver = SsdDriver()

    def run(self, *args, **kwarg):
        self.driver.read(int(args[0]))

        return get_ssd_result()
