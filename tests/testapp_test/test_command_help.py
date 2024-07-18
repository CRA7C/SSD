import sys
import io
import unittest
from testapp.command import HelpCommand


class TestHelp(unittest.TestCase):
    def test_run(self):
        command = HelpCommand()
        sys_stdout = sys.stdout  # 원래의 sys.stdout을 저장
        sys.stdout = io.StringIO()
        command.run()
        help_output = sys.stdout.getvalue()
        sys.stdout = sys_stdout
        for key in ['write', 'read', 'exit', 'help', 'fullwrite', 'fullread']:
            self.assertTrue(key in help_output)


if __name__ == '__main__':
    unittest.main()
