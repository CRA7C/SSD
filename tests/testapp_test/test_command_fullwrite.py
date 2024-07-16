import unittest
from unittest.mock import patch
from testapp.constants import SSD_SIZE
from testapp.command import FullWrite
from testapp.ssd_driver import SsdDriver


class TestFullWrite(unittest.TestCase):

    @patch.object(SsdDriver, 'write')
    def test_run(self, mock_write):
        test_value = 0x1289CDEF
        FullWrite().run(test_value)
        self.assertEqual(mock_write.call_count, SSD_SIZE)


if __name__ == '__main__':
    unittest.main()
