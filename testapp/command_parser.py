from typing import Any

from testapp import command
from testapp.scripts.test_app1 import TestApp1
from testapp.scripts.test_app2 import TestApp2


class CommandParser:
    cmd_if_dict = {
        "write": {"class": command.Write, "required_args_cnt": 2},
        "read": {"class": command.Read, "required_args_cnt": 1},
        "erase": {"class": command.Erase, "required_args_cnt": 2},
        "erase_range": {"class": command.EraseRange, "required_args_cnt": 2},
        "help": {"class": command.Help, "required_args_cnt": 0},
        "exit": {"class": command.Exit, "required_args_cnt": 0},
        "fullwrite": {"class": command.FullWrite, "required_args_cnt": 1},  # noqa
        "fullread": {"class": command.FullRead, "required_args_cnt": 0},  # noqa
        "testapp1": {"class": TestApp1, "required_args_cnt": 0},
        "testapp2": {"class": TestApp2, "required_args_cnt": 0},
    }

    @classmethod
    def validate_command(cls, cmd) -> bool:
        cmd_list = cmd.split(" ")
        cmd_option = cmd_list[0]
        n_args = len(cmd_list) - 1
        if cmd_option not in cls.cmd_if_dict.keys():
            print("Command does not exist")
            return False

        if cls.cmd_if_dict[cmd_option]['required_args_cnt'] != n_args:
            print("The number of argument does not match")
            return False

        if not cls.cmd_if_dict[cmd_option]["class"].is_valid_args(*cmd_list):
            return False
        return True

    @staticmethod
    def parse_args(cmd: str) -> tuple[str, list[str]] | tuple[str, list[Any]]:
        cmd_list = cmd.split(" ")
        cmd_option = cmd_list[0]
        return (cmd_option, cmd_list[1:]) if len(cmd_list) > 1 else (cmd_option, [])

    @classmethod
    def get_command(cls, cmd_option):
        return cls.cmd_if_dict[cmd_option]["class"]()
