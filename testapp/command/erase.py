from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver

MAXIMUM_ERASE_SIZE_AT_ONCE = 10


class Erase(CommandInterface):
    def __init__(self):
        self.driver = SsdDriver()

    def run(self, lba, total_size):
        erase_size = int(total_size)
        initial_lba = int(lba)
        end_lba = 100 if initial_lba + erase_size > 100 else initial_lba + erase_size
        remain_erase_size = end_lba - initial_lba
        for start_lba in range(initial_lba, end_lba, MAXIMUM_ERASE_SIZE_AT_ONCE):
            if remain_erase_size > MAXIMUM_ERASE_SIZE_AT_ONCE:
                size = MAXIMUM_ERASE_SIZE_AT_ONCE
                remain_erase_size -= size
            else:
                size = remain_erase_size
                remain_erase_size = 0
            self.driver.erase(start_lba, size)
