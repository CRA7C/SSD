from unittest import TestCase
from unittest.mock import Mock

from testapp.command import Read, Write
from testapp.command.__interface import CommandInterface


class TestRead(TestCase):
    def setUp(self):
        print("Start Test")
        self.command = Read()

    def tearDown(self):
        print("End Test")
        print("")

    # read     3
    def test_argument_greater_than_99(self):
        with self.assertRaises(ValueError):
            self.command.run(100)

    def test_argument_less_than_0(self):
        with self.assertRaises(ValueError):
            self.command.run(0)

    def test_minus_argument(self):
        with self.assertRaises(ValueError):
            self.command.run(-1)

    def test_run(self):
        test_value = '0x12345678'
        Write().run(3, test_value)
        ret = self.command.run(3)
        self.assertEqual(ret, test_value)
