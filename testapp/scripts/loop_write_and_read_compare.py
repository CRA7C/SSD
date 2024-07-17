from random import randint
from testapp.command.__interface import CommandInterface
from testapp.command import Write, Read
from testapp.constants import SSD_START_LBA, SSD_END_LBA, SSD_MAX_VALUE, SSD_MIN_VALUE


class Loop_WriteAndReadCompare(CommandInterface):  # noqa
    def run(self) -> bool:
        for _ in range(10):
            lba, value = randint(SSD_START_LBA, SSD_END_LBA), randint(SSD_MIN_VALUE, SSD_MAX_VALUE)
            Write().run(lba, value)
            read_value = Read().run(lba)
            if value != int(read_value, 16):
                return False
        return True
