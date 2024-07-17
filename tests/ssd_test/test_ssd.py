from unittest import TestCase
from unittest.mock import Mock, patch

from ssd.nand_driver import NandDriver
from ssd.result_manager import ResultManager
from ssd.solidstatedrive import SolidStateDrive


class TestSSD(TestCase):

    def setUp(self):
        self.ssd = SolidStateDrive()

    def test_write(self):
        self.ssd.nand_driver = Mock(spec=NandDriver)

        self.ssd.write(3, 0x1298CDEF)

        self.ssd.nand_driver.write.assert_called_once()

    @patch.object(NandDriver, 'read', return_value=0xAAAABBBB)
    def test_read(self, _):
        self.ssd.result_manager = Mock(spec=ResultManager)
        lba, expected = 2, '0xAAAABBBB'

        self.ssd.read(lba)

        self.ssd.nand_driver.read.assert_called_with(lba)
        self.ssd.result_manager.write.assert_called_with(expected)

    def test_erase(self):
        self.ssd.nand_driver = Mock(spec=NandDriver)

        self.ssd.erase(3, 2)

        self.ssd.nand_driver.erase.assert_called_once()
