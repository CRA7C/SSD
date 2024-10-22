from unittest import TestCase
from unittest.mock import patch

from testapp.command.erase import EraseCommand
from testapp.ssd_driver import SsdDriver


class TestErase(TestCase):
    def setUp(self):
        self.cmd = EraseCommand()

    @patch.object(SsdDriver, 'erase')
    def test_run(self, mock_erase):
        self.cmd.run('0', '5')
        mock_erase.assert_called_with(0, 5)

    @patch.object(SsdDriver, 'erase')
    def test_run_when_erase_size_greater_than_10(self, mock_erase):
        self.cmd.run('0', '33')
        self.assertEqual(4, mock_erase.call_count)
        mock_erase.assert_called_with(30, 3)

    @patch.object(SsdDriver, 'erase')
    def test_run_when_erase_size_greater_than_100(self, mock_erase):
        self.cmd.run('85', '110')
        self.assertEqual(2, mock_erase.call_count)
        mock_erase.assert_called_with(95, 5)
