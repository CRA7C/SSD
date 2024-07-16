import sys
from unittest import TestCase

from ssd.__main__ import SSDRunner
from ssd.nand_driver import NandDriver, NAND_FILE_PATH
from ssd.result_manager import RESULT_FILE_PATH


class TestSSDRunner(TestCase):
    def setUp(self):
        self.runner = SSDRunner()
        NandDriver.initiate_nand_file(NAND_FILE_PATH)

    def test_run_ssd_write_and_read(self):
        sys.argv = ['test', 'W', '20', '0x1289CDEF']
        self.runner.run()

        sys.argv = ['test', 'R', '20']
        self.runner.run()
        with open(RESULT_FILE_PATH, 'r') as f:
            actual = f.read()

        self.assertEqual('0x1289CDEF', actual)
