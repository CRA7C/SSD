import unittest
from unittest.mock import patch
from testapp.command import Write
from testapp.ssd_driver import SsdDriver


class TestWrite(unittest.TestCase):
    @patch.object(SsdDriver, 'write')
    def test_run(self, mock_write):
        Write().run(20, 0x1289CDEF)
        mock_write.assert_called_once_with(20, 0x1289CDEF)


if __name__ == '__main__':
    unittest.main()
