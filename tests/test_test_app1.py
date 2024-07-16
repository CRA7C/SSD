from unittest import TestCase
from testapp.test_app1 import TestApp1

class TestTestApp(TestCase):
    def test_run(self):
        test_app1 = TestApp1()

        self.assertTrue(test_app1.run())

