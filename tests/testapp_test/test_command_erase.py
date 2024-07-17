from unittest import TestCase

from testapp.command.erase import Erase


class TestErase(TestCase):
    def test_run(self):
        self.cmd = Erase()
        self.cmd.run()
