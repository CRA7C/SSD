from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver

MAXIMUM_ERASE_SIZE_AT_ONCE = 10


class EraseRange(CommandInterface):
    def __init__(self):
        self.driver = SsdDriver()

    def run(self, start_lba: str, end_lba: str):
        remain_erase_size = int(end_lba) - int(start_lba)
        for lba in range(int(start_lba), int(end_lba), MAXIMUM_ERASE_SIZE_AT_ONCE):
            if remain_erase_size > MAXIMUM_ERASE_SIZE_AT_ONCE:
                size = MAXIMUM_ERASE_SIZE_AT_ONCE
                remain_erase_size -= size
            else:
                size = remain_erase_size
                remain_erase_size = 0
            self.driver.erase(lba, size)
