import re
from typing import Tuple, Optional, List

from testapp import command
from testapp.constants import SSD_START_LBA, SSD_END_LBA, SSD_MIN_VALUE, SSD_MAX_VALUE
from testapp.scripts.test_app1 import TestApp1
from testapp.scripts.test_app2 import TestApp2


def is_in_range_lba(lba: str) -> bool:
    try:
        num = int(lba)
        return SSD_START_LBA <= num <= SSD_END_LBA
    except ValueError:
        return False


def is_valid_hex(s: str):
    # 정규식으로 형식을 먼저 확인
    if re.fullmatch(r"0x[0-9A-Fa-f]{8}", s):
        try:
            # 16진수로 변환하여 범위를 확인
            num = int(s, 16)
            return SSD_MIN_VALUE <= num <= SSD_MAX_VALUE
        except ValueError:
            return False
    return False


class CommandParser:
    cmd_if_dict = {
        "write": {"class": command.Write, "required_args_cnt": 2},
        "read": {"class": command.Read, "required_args_cnt": 1},
        "exit": {"class": command.Exit, "required_args_cnt": 0},
        "help": {"class": command.Help, "required_args_cnt": 0},
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
        return True

    @staticmethod
    def parse_args(cmd: str) -> Tuple[str, Optional[List[int]]]:
        cmd_list = cmd.split(" ")
        cmd_option = cmd_list[0]
        if len(cmd_list) > 1:
            cmd_args: list = cmd_list[1:]
            if cmd_option == "read":
                cmd_args[0] = int(cmd_args[0])
            elif cmd_option == "write":
                cmd_args[0] = int(cmd_args[0])
                cmd_args[1] = int(cmd_args[1], 16)
            elif cmd_option == "fullwrite":
                cmd_args[0] = int(cmd_args[0], 16)
            return cmd_option, cmd_args
        return cmd_option, []

    @classmethod
    def get_command(cls, cmd_option):
        return cls.cmd_if_dict[cmd_option]["class"]()
