import unittest
from tests.util import get_ssd_result
from testapp.command import FullWrite, Read


class TestFullWrite(unittest.TestCase):
    def test_run(self):
        test_value = 0x1289CDEF
        FullWrite().run(test_value)
        for result in get_ssd_result().split():
            self.assertEqual(test_value, int(result))


if __name__ == '__main__':
    unittest.main()
