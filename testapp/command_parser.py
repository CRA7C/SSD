from typing import Any

from testapp import command
from testapp.util import is_in_range_lba, is_valid_hex


def is_valid_size(size: str) -> bool:
    try:
        num = int(size)
        return 1 <= num
    except ValueError:
        return False


class CommandParser:
    cmd_if_dict = {
        "write": {"class": command.Write, "required_args_cnt": 2},
        "read": {"class": command.Read, "required_args_cnt": 1},
        "erase": {"class": command.Erase, "required_args_cnt": 2},
        "erase_range": {"class": command.EraseRange, "required_args_cnt": 2},
        "help": {"class": command.Help, "required_args_cnt": 0},
        "exit": {"class": command.Exit, "required_args_cnt": 0},
        "fullwrite": {"class": command.FullWrite, "required_args_cnt": 1},  # noqa
        "fullread": {"class": command.FullRead, "required_args_cnt": 0},
    }

    @classmethod
    def is_predefined_command(cls, name) -> bool:
        if name in cls.cmd_if_dict.keys():
            return True
        return False

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

        if cmd_option == "write":
            n_lba = cmd_list[1]
            value = cmd_list[2]
            if not is_in_range_lba(n_lba):
                return False
            if not is_valid_hex(value):
                return False
            return True

        if cmd_option == "read":
            n_lba = cmd_list[1]
            return True if is_in_range_lba(n_lba) else False

        if cmd_option == "fullwrite":
            value = cmd_list[1]
            return True if is_valid_hex(value) else False

        if cmd_option == "erase":
            n_lba = cmd_list[1]
            size = cmd_list[2]
            if not is_in_range_lba(n_lba):
                return False
            if not is_valid_size(size):
                return False

        if cmd_option == "erase_range":
            start_lba = cmd_list[1]
            end_lba = cmd_list[2]
            if not (is_in_range_lba(start_lba) and is_in_range_lba(end_lba)):
                return False
            if int(start_lba) >= int(end_lba):
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
