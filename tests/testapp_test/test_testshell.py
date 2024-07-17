from unittest import TestCase
from unittest.mock import patch

from testapp.command import Read, Write, FullRead, FullWrite
from testapp.ssd_driver import SsdDriver
from testapp.testshell import TestShell, EXECUTE_INVALID, EXECUTE_VALID_WO_ARGS, EXECUTE_VALID_WITH_ARGS


class TestTestShell(TestCase):
    # 클래스 변수로 테스트 순서 추적
    @classmethod
    def setUpClass(cls):
        cls.test_counter = 0

    def setUp(self):
        super().setUp()
        self.ts = TestShell()
        TestTestShell.test_counter += 1

    @patch.object(FullRead, "run", return_value="GOOD")
    def test_testshell_wo_args(self, mk_fullread):
        cmd_list = ["help", "fullread"]
        for idx, cmd in enumerate(cmd_list):
            with self.subTest(idx=idx, cmd=cmd):
                ret = self.ts.execute(cmd)
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
                ret = self.ts.execute(cmd)
                self.assertEqual(ret, EXECUTE_VALID_WITH_ARGS)

    def test_testshell_invalid(self):
        cmd = "Write 1 dd"

        ret = self.ts.execute(cmd)

        self.assertEqual(ret, EXECUTE_INVALID)

    @patch.object(SsdDriver, "run_subprocess")
    def test_execute_read_command(self, mock_read):
        self.ts.execute("read 3")
        mock_read.assert_called_with("ssd R 3")

    @patch.object(SsdDriver, "run_subprocess")
    def test_execute_write_command(self, mock_write):
        self.ts.execute("write 3 0xAAAABBBB")
        mock_write.assert_called_with("ssd W 3 0xAAAABBBB")
