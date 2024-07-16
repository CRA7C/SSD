from unittest import TestCase
from testapp.test_app1 import TestApp1

class TestTestApp(TestCase):
    def test_run(self):
        test_app1 = TestApp1()
        self.assertTrue(test_app1.run())

    def test_validate_data(self):
        test_app1 = TestApp1()
        read_data = [0x12345678] * 100

        self.assertTrue(test_app1.validate_data(read_data))



