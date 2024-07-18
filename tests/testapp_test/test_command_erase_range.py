from unittest import TestCase
from unittest.mock import patch

from testapp.command.erase_range import EraseRangeCommand
from testapp.ssd_driver import SsdDriver


class TestEraseRange(TestCase):
    def setUp(self):
        self.cmd = EraseRangeCommand()

    @patch.object(SsdDriver, 'erase')
    def test_run_small_range(self, mock_erase):
        self.cmd.run('0', '5')
        mock_erase.assert_called_with(0, 5)

    @patch.object(SsdDriver, 'erase')
    def test_run_large_range(self, mock_erase):
        self.cmd.run('0', '55')
        self.assertEqual(6, mock_erase.call_count)
        mock_erase.assert_called_with(50, 5)
