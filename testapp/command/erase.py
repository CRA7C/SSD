from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver


class Erase(CommandInterface):
    def __init__(self):
        self.driver = SsdDriver()

    def run(self, lba, total_size):
        erase_size = int(total_size)
        remain_erase_size = erase_size
        initial_lba = int(lba)
        for start_lba in range(initial_lba, initial_lba + erase_size, 10):
            if remain_erase_size > 10:
                size = 10
                remain_erase_size -= size
            else:
                size = remain_erase_size
                remain_erase_size = 0
            self.driver.erase(start_lba, size)
