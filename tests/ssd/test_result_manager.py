from unittest import TestCase
from unittest.mock import mock_open, patch

from ssd.result_manager import ResultManager


class TestResultManager(TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_write(self, mock_write):
        self.manager = ResultManager()

        self.manager.write('0x1289CDEF')

        mock_write().write.assert_called_with('0x1289CDEF')
