from unittest import TestCase
from unittest.mock import patch

from testapp.command.flush import Flush
from testapp.ssd_driver import SsdDriver


class TestFlush(TestCase):
    @patch.object(SsdDriver, 'flush')
    def test_run(self, mock_flush):
        self.cmd = Flush()
        self.cmd.run()
        mock_flush.assert_called_once()
