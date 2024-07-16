from unittest import TestCase
from testapp.test_app1 import TestApp1
from testapp.test_app1 import READ_VALUE


class TestTestApp(TestCase):
    def setUp(self):
        super().setUp()
        self.test_app1 = TestApp1()

    def test_run(self):
        self.assertTrue(self.test_app1.run())

    def test_validate_data(self):
        read_data = [READ_VALUE] * 100
        self.assertTrue(self.test_app1.validate_data(read_data))

