from unittest import TestCase
from unittest.mock import patch

from testapp.command import Read, Write
from testapp.test_app2 import TestApp2


class TestTestApp2(TestCase):

    def setUp(self):
        super().setUp()
        self.test_app2 = TestApp2()

    @patch.object(Write, 'run', return_value=True)
    def test_write_30_times(self, write_mock):
        self.assertTrue(self.test_app2.write_30_times())

    @patch.object(Write, 'run', return_value=True)
    def test_write_30_times_SHOULD_execute_write_30_times(self, write_mock):
        self.test_app2.write_30_times()
        self.assertEqual(30, write_mock.call_count)

    @patch.object(Write, 'run', return_value=True)
    def test_over_write_SHOULD_execute_write_6_times(self, write_mock):
        self.test_app2.over_write()
        self.assertEqual(6, write_mock.call_count)

    @patch.object(Read, 'run', return_value=0x12345678)
    def test_read_SHOULD_execute_read_6_times(self, read_mock):
        self.test_app2.read()
        self.assertEqual(6, read_mock.call_count)
