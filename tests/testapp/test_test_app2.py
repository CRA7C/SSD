import unittest
from unittest import TestCase
from unittest.mock import patch

from testapp.command import Read, Write
from testapp.test_app2 import TestApp2, READ_VALUE, WRITE_VALUE


class TestTestApp2(TestCase):

    def setUp(self):
        super().setUp()
        self.test_app2 = TestApp2()

    @patch.object(Write, 'run', return_value=True)
    def test_write_30_times_SHOULD_execute_write_30_times(self, write_mock):
        self.test_app2.write_30_times()
        self.assertEqual(30, write_mock.call_count)

    @patch.object(Write, 'run', return_value=True)
    def test_over_write_SHOULD_execute_write_6_times(self, write_mock):
        self.test_app2.over_write()
        self.assertEqual(6, write_mock.call_count)

    @patch.object(Read, 'run', return_value=READ_VALUE)
    def test_read_SHOULD_execute_read_6_times(self, read_mock):
        self.test_app2.read_data()
        self.assertEqual(6, read_mock.call_count)

    def test_validate_SHOULD_return_True_When_normal_value(self):
        self.assertTrue(self.test_app2.validate([READ_VALUE] * 6))

    def test_validate_SHOULD_return_True_When_wrong_value(self):
        self.assertFalse(self.test_app2.validate([WRITE_VALUE] * 6))

    @patch.object(Write, 'run', return_value=True)
    @patch.object(Read, 'run', return_value=READ_VALUE)
    def test_run_SHOULD_return_True_When_normal(self, read_mock, write_mock):
        self.assertTrue(self.test_app2.run())

    @patch.object(Write, 'run', return_value=True)
    @patch.object(Read, 'run', return_value=WRITE_VALUE)
    def test_run_SHOULD_return_True_When_wrong(self, read_mock, write_mock):
        self.assertFalse(self.test_app2.run())


if __name__ == '__main__':
    unittest.main()