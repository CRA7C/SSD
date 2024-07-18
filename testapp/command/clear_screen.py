import os

from testapp.command.__interface import CommandInterface


class ClearScreenCommand(CommandInterface):
    """
    Exit 클래스는 프로그램을 종료하는 명령어를 구현합니다.
    """
    required_args_cnt: int = 0

    def run(self):
        os.system('cls')

    @staticmethod
    def is_valid_args(*args) -> bool:
        """
        주어진 인자가 유효한지 확인합니다.
        """
        return True
