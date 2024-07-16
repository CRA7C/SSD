import builtins
from unittest import TestCase
from unittest.mock import patch, mock_open

from ssd.nand_driver import NandDriver


class TestNandDriver(TestCase):
    def setUp(self):
        self.driver = NandDriver()

    @patch("builtins.open", new_callable=mock_open,
           read_data='0x00000000\n0x00000000\n0x00000000\n0x1298CDEF\n0x00000000')
    def test_read(self, _):
        self.assertEqual(0x1298CDEF, self.driver.read(3))

    @patch("builtins.open")
    def test_write(self, _):
        self.driver.write(3, 0x1298CDEF)

        self.assertEqual(builtins.open.call_count, 2)
        builtins.open.assert_called_with(self.driver.nand_file_path, 'w')

    def test_write_value(self):
        fake_nand = '0x00000000\n0x00000000\n0x00000000'
        expected = '0x00000000\n0x1298CDEF\n0x00000000'

        actual = self.driver.write_value(fake_nand, 1, 0x1298CDEF)

        self.assertEqual(expected, actual)