from unittest import TestCase
from unittest.mock import patch

from testapp.command import FullRead, FullWrite
from testapp.test_app1 import TestApp1
from testapp.test_app1 import READ_VALUE
from utils.util_log import print_function_name


class TestTestApp1(TestCase):
    def setUp(self):
        super().setUp()
        self.test_app1 = TestApp1()

    @print_function_name
    @patch.object(FullWrite, 'run', return_value=True)
    @patch.object(FullRead, 'run', return_value=[f'0x{READ_VALUE:02x}'] * 100)
    def test_run_SHOULD_RETURN_True_WHEN_normal(self, full_read_mock, full_write_mock):
        self.assertTrue(self.test_app1.run())

    @print_function_name
    @patch.object(FullWrite, 'run', return_value=False)
    @patch.object(FullRead, 'run', return_value=[str(READ_VALUE)] * 100)
    def test_run_SHOULD_RETURN_FALSE_WHEN_write_fail(self, full_read_mock, full_write_mock):
        self.assertFalse(self.test_app1.run())

    @print_function_name
    @patch.object(FullWrite, 'run', return_value=True)
    @patch.object(FullRead, 'run', return_value=['0x00000000'] * 100)
    def test_run_SHOULD_RETURN_FALSE_WHEN_not_match_read_and_write(self, full_read_mock, full_write_mock):
        self.assertFalse(self.test_app1.run())

    @print_function_name
    def test_validate_data(self):
        read_data = [f'0x{READ_VALUE:02x}'] * 100
        self.assertTrue(self.test_app1.validate_data(read_data))
