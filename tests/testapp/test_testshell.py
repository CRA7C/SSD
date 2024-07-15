from unittest import TestCase

from testapp.testshell import TestShell


class TestTestShell(TestCase):
    def setUp(self):
        super().setUp()
        self.testshell = TestShell()

    def test_testshell_write(self):
        cmd = "write 3 0xAAAABBBB"

        self.testshell.execute(cmd)

        # self.assert

    def test_testshell_read(self):
        cmd = "read 3"

        self.testshell.execute(cmd)

        # self.assert

    def test_testshell_exit(self):
        cmd = "exit"

        self.testshell.execute(cmd)

        # self.assert

    def test_testshell_help(self):
        cmd = "help"

        self.testshell.execute(cmd)

        # self.assert

    def test_testshell_fullwrite(self):
        cmd = "fullwrite 0xABCDFFFF"

        self.testshell.execute(cmd)

        # self.assert

    def test_testshell_fullread(self):
        cmd = "fullread"

        self.testshell.execute(cmd)

        # self.assert

    def test_testshell_testapp1(self):
        cmd = "testapp1"

        self.testshell.execute(cmd)

        # self.assert

    def test_testshell_testapp2(self):
        cmd = "testapp2"

        self.testshell.execute(cmd)

        # self.assert

    def test_testshell_invalid(self):
        cmd = "Write 1 dd"

        self.testshell.execute(cmd)

        # self.assertEqual(ret, "INVALID COMMAND")
