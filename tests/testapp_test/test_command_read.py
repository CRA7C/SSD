from unittest import TestCase
from unittest.mock import patch

from testapp.command import Read
from testapp.ssd_driver import SsdDriver
from utils.util_log import print_function_name


class TestRead(TestCase):
    def setUp(self):
        self.command = Read()

    @print_function_name
    def test_argument_greater_than_99(self):
        with self.assertRaises(ValueError):
            self.command.run(100)

    @print_function_name
    def test_argument_less_than_0(self):
        with self.assertRaises(ValueError):
            self.command.run(-10)

    @print_function_name
    def test_minus_argument(self):
        with self.assertRaises(ValueError):
            self.command.run(-1)

    @print_function_name
    @patch.object(SsdDriver, 'read')
    def test_run(self, mock_read):
        Read().run(3)
        mock_read.assert_called_once_with(3)
