from testapp.command_parser import CommandParser
from testapp.constants import INVALID_COMMAND
from testapp.scripts import get_test_scripts, run_script

EXECUTE_VALID_WO_ARGS = 2
EXECUTE_VALID_WITH_ARGS = 1
EXECUTE_INVALID = 0


class TestShell:

    @staticmethod
    def execute(cmd: str) -> int:
        cmd_option = cmd.split()[0]
        if CommandParser.is_predefined_command(cmd_option):
            cmd_option, cmd_args = CommandParser.parse_args(cmd)
            if not CommandParser.validate_command(cmd):
                print(INVALID_COMMAND)
                return EXECUTE_INVALID
            cmd_if = CommandParser.get_command(cmd_option)
            cmd_if.run(*cmd_args)
            return EXECUTE_VALID_WITH_ARGS if cmd_args else EXECUTE_VALID_WO_ARGS

        else:  # test script 중에 있으면 동작
            ts_dict = get_test_scripts()
            if cmd_option in ts_dict.keys():
                success = run_script(ts_dict[cmd_option])
                print('PASS' if success else 'FAIL!')
                return success
        return EXECUTE_INVALID


def main():
    while True:
        cmd = input("> ")
        if TestShell.execute(cmd) == EXECUTE_INVALID:
            print(INVALID_COMMAND)
