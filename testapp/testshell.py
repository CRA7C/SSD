from testapp.command_parser import CommandParser
from testapp.constants import INVALID_COMMAND

EXECUTE_VALID_WO_ARGS = 2
EXECUTE_VALID_WITH_ARGS = 1
EXECUTE_INVALID = 0


class TestShell:

    @staticmethod
    def execute(cmd: str) -> int:
        if not CommandParser.validate_command(cmd):
            print(INVALID_COMMAND)
            return EXECUTE_INVALID

        cmd_option, cmd_args = CommandParser.parse_args(cmd)
        cmd_if = CommandParser.get_command(cmd_option)
        cmd_if.run(*cmd_args)
        return EXECUTE_VALID_WITH_ARGS if cmd_args else EXECUTE_VALID_WO_ARGS


def main():
    while True:
        cmd = input("> ")
        TestShell.execute(cmd)
