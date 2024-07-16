from unittest import TestCase
from unittest.mock import patch

from testapp.testshell import TestShell, EXECUTE_INVALID, EXECUTE_VALID_WO_ARGS, EXECUTE_VALID_WITH_ARGS
from testapp.command import Read, Write, FullRead, FullWrite, Help


class TestTestShell(TestCase):
    def setUp(self):
        super().setUp()
        self.testshell = TestShell()

    def test_valid_cmd_true(self):
        cmd_list = [
            "write 3 0xAAAABBBB",
            "read 3",
            "help",
            "fullwrite 0xABCDFFFF",
            "fullread",
            "testapp1",
            "testapp2",
        ]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                print(f"{idx + 1}. {cmd}")
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
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                print(f"{idx + 1}. {cmd}")
                ret = self.testshell.valid_cmd(cmd)
                self.assertFalse(ret)

    def test_valid_cmd_read_false(self):

        cmd_list = [
            "read 3 0xAAAABBBB",
            "Read 3",
            "read 0xAAAABBBB",
        ]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                print(f"{idx + 1}. {cmd}")
                ret = self.testshell.valid_cmd(cmd)
                self.assertFalse(ret)

    def test_valid_cmd_exit_false(self):

        cmd_list = [
            "Exit",
            "exit 1",
            "exit 0xABCDFFFF",
        ]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                print(f"{idx + 1}. {cmd}")
                ret = self.testshell.valid_cmd(cmd)
                self.assertFalse(ret)

    def test_valid_cmd_help_false(self):

        cmd_list = [
            "HELP",
            "hELP",
            "help 0xABCDFFFF",
        ]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                print(f"{idx + 1}. {cmd}")
                ret = self.testshell.valid_cmd(cmd)
                self.assertFalse(ret)

    def test_valid_cmd_fullwrite_false(self):

        cmd_list = [
            "Fullwrite 0xABCDFFFF",
            "FULLWRITE 0xABCDFFFF",
            "FullWrite 0xABCDFFFF",
            "fullwrite ABCDFFFF",
        ]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                print(f"{idx + 1}. {cmd}")
                ret = self.testshell.valid_cmd(cmd)
                self.assertFalse(ret)

    def test_valid_cmd_fullread_false(self):

        cmd_list = [
            "Fullread",
            "FULLREAD",
            "FullRead",
        ]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                print(f"{idx + 1}. {cmd}")
                ret = self.testshell.valid_cmd(cmd)
                self.assertFalse(ret)

    @patch.object(TestShell, 'valid_cmd', return_value=True)
    def test_is_valid_cmd_true(self, mk):
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
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                print(f"{idx + 1}. {cmd}")
                ret = self.testshell.is_valid_cmd(cmd)
                self.assertTrue(ret)

    @patch.object(TestShell, 'valid_cmd', return_value=False)
    def test_is_valid_cmd_false(self, mk):
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
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                print(f"{idx + 1}. {cmd}")
                ret = self.testshell.is_valid_cmd(cmd)
                self.assertFalse(ret)

    def test_parse_args(self):
        cmd_dict = {
            "write 3 0xAAAABBBB": ("write", [3, 0xAAAABBBB]),
            "read 3": ("read", [3]),
            "help": ("help", None),
            "fullwrite 0xABCDFFFF": ("fullwrite", [0xABCDFFFF]),
            "fullread": ("fullread", None),
        }
        for idx, (key, val) in enumerate(cmd_dict.items()):
            with self.subTest(idx=idx, key=key, val=val):
                print(f"{idx + 1}. {key},{val}")
                ret = self.testshell.parse_args(key)
                self.assertEqual(ret, val)

    @patch.object(FullRead, "run", return_value="GOOD")
    def test_testshell_wo_args(self, mk_fullread):
        cmd_list = ["help", "fullread"]#, "testapp1", "testapp2", "fullread"]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                print(f"{idx + 1}. {cmd}")
                ret = self.testshell.execute(cmd)
                self.assertEqual(ret, EXECUTE_VALID_WO_ARGS)
    @patch.object(Read, "run", return_value="GOOD")
    def test_testshell_with_args(self, mk_read):
        cmd_list = ["fullwrite 0xABCDFFFF",
                    "read 3",
                    "write 3 0xAAAABBBB"
                    ]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                print(f"{idx + 1}. {cmd}")
                ret = self.testshell.execute(cmd)
                self.assertEqual(ret, EXECUTE_VALID_WITH_ARGS)

    def test_testshell_invalid(self):
        cmd = "Write 1 dd"

        ret = self.testshell.execute(cmd)

        self.assertEqual(ret, EXECUTE_INVALID)