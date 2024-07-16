from unittest import TestCase
from unittest.mock import patch

from testapp.test_app1 import TestApp1
from testapp.test_app2 import TestApp2
from testapp.testshell import TestShell, EXECUTE_INVALID, EXECUTE_VALID_WO_ARGS, EXECUTE_VALID_WITH_ARGS
from testapp.command import Read, Write, FullRead, FullWrite


class TestTestShell(TestCase):
    # 클래스 변수로 테스트 순서 추적
    @classmethod
    def setUpClass(cls):
        cls.test_counter = 0

    def setUp(self):
        super().setUp()
        self.testshell = TestShell()
        TestTestShell.test_counter += 1
        print(f"\nRunning test #{TestTestShell.test_counter}")

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

    @patch.object(TestApp2, "run", return_value=True)
    @patch.object(TestApp1, "run", return_value=True)
    @patch.object(FullRead, "run", return_value="GOOD")
    def test_testshell_wo_args(self, mk_fullread, mk_testapp1, mk_testapp2):
        cmd_list = ["help", "fullread", "testapp1", "testapp2"]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                print(f"{idx + 1}. {cmd}")
                ret = self.testshell.execute(cmd)
                self.assertEqual(ret, EXECUTE_VALID_WO_ARGS)

    @patch.object(Write, "run", return_value="GOOD")
    @patch.object(Read, "run", return_value="GOOD")
    @patch.object(FullWrite, "run", return_value="GOOD")
    def test_testshell_with_args(self, mk_fullwrite, mk_read, mk_write):
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
