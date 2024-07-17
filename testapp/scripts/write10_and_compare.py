from testapp.command.__interface import CommandInterface
from testapp.command import Write, Read


class Write10AndCompare(CommandInterface):
    def run(self) -> bool:
        lba, value = 3, 0x12345678
        for _ in range(10):
            Write().run(lba, value)
            read_value = Read().run(lba)
            if value != int(read_value, 16):
                return False
        return True
