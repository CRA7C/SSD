from unittest import TestCase
from unittest.mock import patch

from testapp.testshell import TestShell


class TestTestShell(TestCase):
    def setUp(self):
        super().setUp()
        self.testshell = TestShell()

    def test_valid_cmd_true(self):
        cmd_list = [
            "write 3 0xAAAABBBB",
            "read 3",
            "exit",
            "help",
            "fullwrite 0xABCDFFFF",
            "fullread",
            "testapp1",
            "testapp2",
        ]
        for cmd in cmd_list:
            ret = self.testshell.valid_cmd(cmd)
            self.assertTrue(ret)

    def test_valid_cmd_write_false(self):

        cmd_list = [
            "Write 3 0xAAAABBBB",
            "Write 3 0xAAAABBBB",
            "write 0xAAAABBBB",
            "write 3",
            "write",
        ]
        for cmd in cmd_list:
            ret = self.testshell.valid_cmd(cmd)
            self.assertFalse(ret)

    def test_valid_cmd_read_false(self):

        cmd_list = [
            "read 3 0xAAAABBBB",
            "Read 3",
            "read 0xAAAABBBB",
        ]
        for cmd in cmd_list:
            ret = self.testshell.valid_cmd(cmd)
            self.assertFalse(ret)

    def test_valid_cmd_exit_false(self):

        cmd_list = [
            "Exit",
            "exit 1",
            "exit 0xABCDFFFF",
        ]
        for cmd in cmd_list:
            ret = self.testshell.valid_cmd(cmd)
            self.assertFalse(ret)

    def test_valid_cmd_help_false(self):

        cmd_list = [
            "HELP",
            "hELP",
            "help 0xABCDFFFF",
        ]
        for cmd in cmd_list:
            ret = self.testshell.valid_cmd(cmd)
            self.assertFalse(ret)

    def test_valid_cmd_fullwrite_false(self):

        cmd_list = [
            "Fullwrite 0xABCDFFFF",
            "FULLWRITE 0xABCDFFFF",
            "FullWrite 0xABCDFFFF",
            "fullwrite ABCDFFFF",
        ]
        for cmd in cmd_list:
            ret = self.testshell.valid_cmd(cmd)
            self.assertFalse(ret)

    def test_valid_cmd_fullread_false(self):

        cmd_list = [
            "Fullread",
            "FULLREAD",
            "FullRead",
        ]
        for cmd in cmd_list:
            ret = self.testshell.valid_cmd(cmd)
            self.assertFalse(ret)

    @patch.object(TestShell, 'valid_cmd', return_value=True)
    def test_convert_to_valid_cmd_true(self):
        cmd_list = [
            "write 3 0xAAAABBBB",
            "read 3",
            "exit",
            "help",
            "fullwrite 0xABCDFFFF",
            "fullread",
            "testapp1",
            "testapp2",
        ]
        for cmd in cmd_list:
            ret = self.testshell.convert_to_valid_cmd(cmd)
            self.assertEqual(ret, cmd)

    @patch.object(TestShell, 'valid_cmd', return_value=False)
    def test_convert_to_valid_cmd_false(self):
        cmd_list = [
            "write 3 0xAAAABBBB",
            "read 3",
            "exit",
            "help",
            "fullwrite 0xABCDFFFF",
            "fullread",
            "testapp1",
            "testapp2",
        ]
        for cmd in cmd_list:
            ret = self.testshell.convert_to_valid_cmd(cmd)
            self.assertEqual(ret, "INVALID COMMAND")

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
