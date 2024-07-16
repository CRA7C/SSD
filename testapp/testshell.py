from testapp.command_parser import CommandParser
from testapp.constants import (INVALID_COMMAND)

EXECUTE_VALID_WO_ARGS = 2
EXECUTE_VALID_WITH_ARGS = 1
EXECUTE_INVALID = 0


class TestShell:

    def execute(self, cmd: str) -> int:
        if not CommandParser.validate_command(cmd):
            print(INVALID_COMMAND)
            return EXECUTE_INVALID

        cmd_option, cmd_args = CommandParser.parse_args(cmd)

        cmd_if = CommandParser.cmd_if_dict[cmd_option]()
        if cmd_args is not None:
            print(cmd_option, *cmd_args)
            cmd_if.run(*cmd_args)
            return EXECUTE_VALID_WITH_ARGS

        print(cmd_option)
        cmd_if.run()
        return EXECUTE_VALID_WO_ARGS


def main():
    ts = TestShell()
    while True:
        cmd = input("> ")
        ts.execute(cmd)
