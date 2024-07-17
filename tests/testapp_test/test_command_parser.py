from unittest import TestCase

from testapp.command_parser import CommandParser


class TestCommandParser(TestCase):

    def setUp(self):
        self.parser = CommandParser()

    def test_valid_cmd_true(self):
        cmd_list = [
            "write 3 0xAAAABBBB",
            "read 3",
            "help",
            "fullwrite 0xABCDFFFF",
            "fullread",
        ]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                ret = self.parser.validate_command(cmd)
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
                ret = self.parser.validate_command(cmd)
                self.assertFalse(ret)

    def test_valid_cmd_read_false(self):

        cmd_list = [
            "read 3 0xAAAABBBB",
            "Read 3",
            "read 0xAAAABBBB",
        ]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                ret = self.parser.validate_command(cmd)
                self.assertFalse(ret)

    def test_valid_cmd_exit_false(self):

        cmd_list = [
            "Exit",
            "exit 1",
            "exit 0xABCDFFFF",
        ]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                ret = self.parser.validate_command(cmd)
                self.assertFalse(ret)

    def test_valid_cmd_help_false(self):

        cmd_list = [
            "HELP",
            "hELP",
            "help 0xABCDFFFF",
        ]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                ret = self.parser.validate_command(cmd)
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
                ret = self.parser.validate_command(cmd)
                self.assertFalse(ret)

    def test_valid_cmd_fullread_false(self):

        cmd_list = [
            "Fullread",
            "FULLREAD",
            "FullRead",
        ]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                ret = self.parser.validate_command(cmd)
                self.assertFalse(ret)

    def test_parse_args(self):
        cmd_dict = {
            "write 3 0xAAAABBBB": ("write", ['3', '0xAAAABBBB']),
            "read 3": ("read", ['3']),
            "help": ("help", []),
            "fullwrite 0xABCDFFFF": ("fullwrite", ['0xABCDFFFF']),
            "fullread": ("fullread", []),
        }
        for idx, (key, val) in enumerate(cmd_dict.items()):
            with self.subTest(idx=idx, key=key, val=val):
                ret = self.parser.parse_args(key)
                self.assertEqual(ret, val)
