import unittest
from unittest import TestCase
from unittest.mock import patch

from testapp.command import FullRead
from testapp.constants import SSD_SIZE
from testapp.ssd_driver import SsdDriver


class Test(TestCase):
    def setUp(self):
        self.command = FullRead()

    def test_with_argument(self):
        with self.assertRaises(TypeError):
            self.command.run(100)  # noqa

    @patch.object(SsdDriver, 'read')
    def test_read_count(self, mock_read):
        self.command.run()
        self.assertEqual(mock_read.call_count, SSD_SIZE)


if __name__ == '__main__':
    unittest.main()
