import unittest
from testapp.command.__interface import CommandInterface


class TestCommandInterface(unittest.TestCase):
    def test_command_interface(self):
        with self.assertRaises(TypeError):
            command = CommandInterface()  # 추상 메서드이기에 에러 발생
            command.run()


if __name__ == '__main__':
    unittest.main()
