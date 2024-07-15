import unittest
import subprocess
from pathlib import Path
from unittest.mock import patch
from testapp.ssd_driver import SsdDriver


class TestSsdDriver(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.driver = SsdDriver()

    @patch('subprocess.run')
    def test_run_command(self, mock_run):
        # 모킹된 subprocess.run의 반환값 설정
        mock_run.return_value.stdout = "Command output"
        mock_run.return_value.stderr = ""

        command = "ls"
        stdout, stderr = self.driver._run("ssd R 2")

        # subprocess.run이 올바른 인자와 함께 호출되었는지 확인
        mock_run.assert_called_once_with(
            command,
            shell=True,
            cwd=Path(__file__).parent.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        self.assertEqual(stdout, "Command output")
        self.assertEqual(stderr, "")

    @patch('testapp.ssd_driver.SsdDriver._run')
    def test_read(self, mock_run):
        test_lba = 3
        expected_command = f"ssd R {test_lba}"
        self.driver.read(test_lba)
        mock_run._run.assert_called_once_with(expected_command)

    @patch('testapp.ssd_driver.SsdDriver._run')
    def test_write(self, mock_run):
        test_lba = 3
        test_value = 0x1289CDEF
        expected_command = f"ssd R {test_lba} 0x{test_value:08X}"
        self.driver.write(test_lba, test_value)
        mock_run._run.assert_called_once_with(expected_command)
