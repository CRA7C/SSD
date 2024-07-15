import unittest
from tests.util import run_subprocess


class TestSsdDriver(unittest.TestCase):
    def ssd_read(self, lba, data):
        run_subprocess(f"ssd R {lba}")

    def ssd_write(self, lba, data):
        run_subprocess(f"ssd W {lba} 0x{data:08X}")
