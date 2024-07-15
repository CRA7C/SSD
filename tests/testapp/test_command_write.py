import unittest
from tests.util import get_ssd_result
from testapp.command import Write, Read


class TestFullWrite(unittest.TestCase):
    def test_run(self):
        Write().run(20, 0x1289CDEF)
        ret = Read().run(20)
        result = get_ssd_result()
        self.assertEqual(int(ret), int(result))


if __name__ == '__main__':
    unittest.main()
