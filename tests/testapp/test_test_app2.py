from unittest import TestCase
from unittest.mock import patch

from testapp.command import Read, Write
from testapp.test_app2 import TestApp2


class TestTestApp2(TestCase):

    @patch.object(Write, 'run', return_value=True)
    def test_write_30_times(self, write_mock):
        self.test_app2 = TestApp2()
        self.assertTrue(self.test_app2.write_30_times())

    @patch.object(Write, 'run', return_value=True)
    def test_write_30_times_SHOULD_execute_write_30_times(self, write_mock):
        self.test_app2 = TestApp2()
        self.test_app2.write_30_times()

        self.assertEqual(30, write_mock.call_count)


