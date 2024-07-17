from testapp.command.__interface import CommandInterface
from testapp.command import FullRead


class FullRead10AndCompare(CommandInterface):
    def run(self) -> bool:
        init_data = FullRead().run()
        for _ in range(9):
            test_data = FullRead().run()
            if init_data != test_data:
                return False
        return True
