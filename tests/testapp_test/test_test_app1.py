from unittest import TestCase
from unittest.mock import patch

from testapp.command import FullReadCommand, FullWriteCommand
from testapp.scripts.test_app1 import TestApp1
from testapp.scripts.test_app1 import READ_VALUE
from my_logger.util_log import print_function_name


class TestTestApp1(TestCase):
    def setUp(self):
        super().setUp()
        self.test_app1 = TestApp1()

    @print_function_name
    @patch.object(FullWriteCommand, 'run', return_value=True)
    @patch.object(FullReadCommand, 'run', return_value=[f'0x{READ_VALUE:02x}'] * 100)
    def test_run_SHOULD_RETURN_True_WHEN_normal(self, full_read_mock, full_write_mock):
        self.assertTrue(self.test_app1.run())

    @print_function_name
    @patch.object(FullWriteCommand, 'run', return_value=False)
    @patch.object(FullReadCommand, 'run', return_value=[str(READ_VALUE)] * 100)
    def test_run_SHOULD_RETURN_FALSE_WHEN_write_fail(self, full_read_mock, full_write_mock):
        self.assertFalse(self.test_app1.run())

    @print_function_name
    @patch.object(FullWriteCommand, 'run', return_value=True)
    @patch.object(FullReadCommand, 'run', return_value=['0x00000000'] * 100)
    def test_run_SHOULD_RETURN_FALSE_WHEN_not_match_read_and_write(self, full_read_mock, full_write_mock):
        self.assertFalse(self.test_app1.run())
