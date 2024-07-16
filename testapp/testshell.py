import re
from typing import Tuple, Optional, List

from testapp import command
from testapp.test_app1 import TestApp1
from testapp.test_app2 import TestApp2
from testapp.constants import (SSD_MIN_VALUE, SSD_MAX_VALUE,
                               SSD_START_LBA, SSD_END_LBA)


EXECUTE_VALID_WO_ARGS = 2
EXECUTE_VALID_WITH_ARGS = 1
EXECUTE_INVALID = 0


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


class TestShell:
    cmd_if_dict = {
        "write": command.Write,
        "read": command.Read,
        "exit": command.Exit,
        "help": command.Help,
        "fullwrite": command.FullWrite,  # noqa
        "fullread": command.FullRead,  # noqa
        "testapp1": TestApp1,
        "testapp2": TestApp2,
    }

    def execute(self, cmd: str) -> int:
        if not self.is_valid_cmd(cmd):
            print(cmd)
            return EXECUTE_INVALID

        cmd_option, cmd_args = self.parse_args(cmd)

        cmd_if = self.cmd_if_dict[cmd_option]()
        if cmd_args is not None:
            print(cmd_option, cmd_args)
            cmd_if.run(*cmd_args)
            return EXECUTE_VALID_WITH_ARGS

        print(cmd_option, cmd_args)
        cmd_if.run()
        return EXECUTE_VALID_WO_ARGS

    def is_valid_cmd(self, cmd: str) -> bool:
        if self.valid_cmd(cmd):
            return True
        else:
            return False

    @staticmethod
    def valid_cmd(cmd) -> bool:
        """
        유효성 검사 수행
        """
        cmd_option_to_args_dict = {
            "write": 2,
            "read": 1,
            "help": 0,
            "fullwrite": 1,
            "fullread": 0,
            "testapp1": 0,
            "testapp2": 0
        }
        cmd_list = cmd.split(" ")
        cmd_option = cmd_list[0]
        n_args = len(cmd_list) - 1
        if cmd_option not in cmd_option_to_args_dict.keys():
            print("Command does not exist")
            return False
        if cmd_option_to_args_dict[cmd_option] != n_args:
            print("The number of argument does not match")
            return False
        # 0. exit (구현 필요 x), help, fullread , testapp1, testapp2
        if n_args == 0:
            return True
        # 1. write
        if cmd_option == "write":
            n_lba = cmd_list[1]
            value = cmd_list[2]
            if not is_in_range_lba(n_lba):
                return False
            if not is_valid_hex(value):
                return False
            return True
        # 2. read
        if cmd_option == "read":
            n_lba = cmd_list[1]
            return True if is_in_range_lba(n_lba) else False

        # 3. fullwrite
        if cmd_option == "fullwrite":
            value = cmd_list[1]
            if is_valid_hex(value):
                return True
            else:
                return False
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
        return cmd_option, None


def main():
    ts = TestShell()
    while True:
        cmd = input("> ")
        if cmd == "exit":
            break
        ts.execute(cmd)
    return


if __name__ == "__main__":
    main()
