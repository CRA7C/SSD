from unittest import TestCase
from unittest.mock import patch

from testapp.command.erase_range import EraseRange
from testapp.ssd_driver import SsdDriver


class TestEraseRange(TestCase):
    @patch.object(SsdDriver, 'erase')
    def test_run_small_range(self, mock_erase):
        self.cmd = EraseRange()
        self.cmd.run('0', '5')
        mock_erase.assert_called_with(0, 5)
