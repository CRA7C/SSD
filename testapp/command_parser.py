from typing import Any

from testapp import command
from my_logger import Logger
from testapp.command.__interface import CommandInterface


class CommandParser:
    """
    CommandParser 클래스는 명령어를 파싱하고 유효성을 검사하며, 적절한 명령어 객체를 반환하는 기능을 제공합니다.
    """
    cmd_if_dict = {
        "write": {"class": command.Write, "required_args_cnt": 2},
        "read": {"class": command.Read, "required_args_cnt": 1},
        "erase": {"class": command.Erase, "required_args_cnt": 2},
        "erase_range": {"class": command.EraseRange, "required_args_cnt": 2},
        "flush": {"class": command.Flush, "required_args_cnt": 0},
        "help": {"class": command.Help, "required_args_cnt": 0},
        "exit": {"class": command.Exit, "required_args_cnt": 0},
        "fullwrite": {"class": command.FullWrite, "required_args_cnt": 1},  # noqa
        "fullread": {"class": command.FullRead, "required_args_cnt": 0},
    }

    @classmethod
    def is_predefined_command(cls, name: str) -> bool:
        """
        주어진 이름이 사전 정의된 명령어인지 확인합니다.

        Args:
            name (str): 확인할 명령어 이름

        Returns:
            bool: 사전 정의된 명령어이면 True, 그렇지 않으면 False
        """
        if name in cls.cmd_if_dict.keys():
            return True
        return False

    @classmethod
    def validate_command(cls, cmd: str) -> bool:
        """
        주어진 명령어의 유효성을 검사합니다.

        Args:
            cmd (str): 검사할 명령어

        Returns:
            bool: 유효한 명령어이면 True, 그렇지 않으면 False
        """
        cmd_list = cmd.split(" ")
        cmd_option = cmd_list[0]
        n_args = len(cmd_list) - 1
        if cmd_option not in cls.cmd_if_dict.keys():
            Logger().debug("Command does not exist")
            return False

        if cls.cmd_if_dict[cmd_option]['required_args_cnt'] != n_args:
            Logger().debug("The number of argument does not match")
            return False

        if not cls.cmd_if_dict[cmd_option]["class"].is_valid_args(*cmd_list):
            return False
        return True

    @staticmethod
    def parse_args(cmd: str) -> tuple[str, list[str]] | tuple[str, list[Any]]:
        """
        주어진 명령어를 파싱하여 옵션과 인자를 반환합니다.

        Args:
            cmd (str): 파싱할 명령어

        Returns:
            tuple[str, list[str]] | tuple[str, list[Any]]: 명령 옵션과 인자 리스트의 튜플
        """
        cmd_list = cmd.split(" ")
        cmd_option = cmd_list[0]
        return (cmd_option, cmd_list[1:]) if len(cmd_list) > 1 else (cmd_option, [])

    @classmethod
    def get_command(cls, cmd_option: str) -> CommandInterface:
        """
        주어진 명령 옵션에 해당하는 명령어 객체를 반환합니다.

        Args:
            cmd_option (str): 명령 옵션

        Returns:
            command.Command: 명령어 객체
        """
        return cls.cmd_if_dict[cmd_option]["class"]()
