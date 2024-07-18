from typing import Any, Dict, Type
from my_logger import Logger
from testapp.command import (WriteCommand, ReadCommand, EraseCommand, EraseRangeCommand,
                             FlushCommand, HelpCommand, ExitCommand,
                             FullWriteCommand, FullReadCommand, ClearScreenCommand)
from testapp.command.__interface import CommandInterface


class CommandFactory:
    """
    명령어 객체를 생성하는 팩토리 클래스입니다.
    """
    _cmd_dict: Dict[str, Type[CommandInterface]] = {
        "write": WriteCommand,
        "read": ReadCommand,
        "erase": EraseCommand,
        "erase_range": EraseRangeCommand,
        "flush": FlushCommand,
        "help": HelpCommand,
        "exit": ExitCommand,
        "fullwrite": FullWriteCommand,
        "fullread": FullReadCommand,
        "cls": ClearScreenCommand,
    }

    @classmethod
    def get_command_instance(cls, cmd_name: str) -> CommandInterface:
        """
        주어진 명령 옵션에 해당하는 명령어 객체를 반환합니다.

        Args:
            cmd_name (str): 명령 이름

        Returns:
            CommandInterface: 명령어 객체
        """
        return cls._cmd_dict[cmd_name]()

    @classmethod
    def get_command_dict(cls):
        return cls._cmd_dict


def is_predefined_command_name(name: str) -> bool:
    """
    주어진 이름이 사전 정의된 명령어인지 확인합니다.

    Args:
        name (str): 확인할 명령어 이름

    Returns:
        bool: 사전 정의된 명령어이면 True, 그렇지 않으면 False
    """
    cmd_dict = CommandFactory.get_command_dict()
    if name in cmd_dict.keys():
        return True
    return False


def validate_command(cmd: str) -> bool:
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
    cmd_dict = CommandFactory.get_command_dict()
    if cmd_option not in CommandFactory.get_command_dict():
        Logger().debug("Command does not exist")
        return False

    if cmd_dict[cmd_option].required_args_cnt != n_args:
        Logger().debug("The number of argument does not match")
        return False

    if not cmd_dict[cmd_option].is_valid_args(*cmd_list):
        return False
    return True


@staticmethod
def parse_cmd_args(cmd: str) -> tuple[str, list[str]] | tuple[str, list[Any]]:
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
