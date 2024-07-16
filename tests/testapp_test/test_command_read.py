from unittest import TestCase
from unittest.mock import patch

from testapp.command import Read
from testapp.ssd_driver import SsdDriver


class TestRead(TestCase):
    def setUp(self):
        print("Start Test")
        self.command = Read()

    def tearDown(self):
        print("End Test")
        print("")

    def test_argument_greater_than_99(self):
        with self.assertRaises(ValueError):
            self.command.run(100)

    def test_argument_less_than_0(self):
        with self.assertRaises(ValueError):
            self.command.run(-10)

    def test_minus_argument(self):
        with self.assertRaises(ValueError):
            self.command.run(-1)

    @patch.object(SsdDriver, 'read')
    def test_run(self, mock_read):
        Read().run(3)
        mock_read.assert_called_once_with(3)
