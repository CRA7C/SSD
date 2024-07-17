from unittest import TestCase
from unittest.mock import patch

from testapp.command.erase import Erase
from testapp.ssd_driver import SsdDriver


class TestErase(TestCase):
    @patch.object(SsdDriver, 'erase')
    def test_run(self, mock_erase):
        self.cmd = Erase()
        self.cmd.run('0', '5')
        mock_erase.assert_called_with(0, 5)

    @patch.object(SsdDriver, 'erase')
    def test_run_when_erase_size_greater_than_10(self, mock_erase):
        self.cmd = Erase()
        self.cmd.run('0', '33')
        self.assertEqual(4, mock_erase.call_count)
        mock_erase.assert_called_with(30, 3)
