import unittest
from unittest import TestCase

from testapp.command import FullRead, FullWrite
from tests.util import get_ssd_result


class Test(TestCase):
    def setUp(self):
        print("Start Test")
        self.command = FullRead()

    def tearDown(self):
        print("End Test")
        print("")

    def test_with_argument(self):
        with self.assertRaises(ValueError):
            self.command.run(100)

    def test_full_read(self):
        test_value = 0x1289CDEF
        FullWrite().run(test_value)

        self.assertEqual(self.command.run(), get_ssd_result())


if __name__ == '__main__':
    unittest.main()