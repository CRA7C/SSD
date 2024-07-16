import sys
from unittest import TestCase
from unittest.mock import patch

from ssd.__main__ import SSDRunner
from ssd.nand_driver import NandDriver, NAND_FILE_PATH
from ssd.result_manager import RESULT_FILE_PATH
from ssd.ssd import SSD


class TestSSDRunner(TestCase):
    def setUp(self):
        self.runner = SSDRunner()
        NandDriver.initiate_nand_file(NAND_FILE_PATH)

    @patch.object(SSD, 'read')
    def test_run_ssd_read(self, _):
        sys.argv = ['test', 'R', '20']

        self.runner.run()

        self.runner.ssd.read.assert_called_with(20)

    @patch.object(SSD, 'write')
    def test_run_ssd_write(self, _):
        sys.argv = ['test', 'W', '20', '0x1289CDEF']

        self.runner.run()

        self.runner.ssd.write.assert_called_with(20, '0x1289CDEF')
