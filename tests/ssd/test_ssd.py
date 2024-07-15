from unittest import TestCase
from unittest.mock import Mock, patch

from ssd.nand_driver import NandDriver
from ssd.ssd import SSD


class TestSSD(TestCase):

    def setUp(self):
        self.ssd = SSD()

    def test_write(self):
        self.ssd.nand_driver = Mock()

        self.ssd.write(3, 0x1298CDEF)

        self.ssd.nand_driver.write.assert_called_once()

    @patch.object(NandDriver, 'read', return_value=0xAAAABBBB)
    def test_read(self, _):
        self.ssd.result_manager = Mock()
        lba = 2
        expected = 0xAAAABBBB

        self.ssd.read(lba)

        self.ssd.nand_driver.read.assert_called_with(lba)
        self.ssd.result_manager.write.assert_called_with(expected)
