from random import randint
from testapp.command.__interface import CommandInterface
from testapp.command import FullRead, FullWrite
from testapp.constants import SSD_MIN_VALUE, SSD_MAX_VALUE


class FullWriteReadCompare(CommandInterface):
    def run(self) -> bool:
        value = randint(SSD_MIN_VALUE, SSD_MAX_VALUE)
        FullWrite().run(value)
        read_data = FullRead().run()
        return all(int(data, 16) == value for data in read_data)
