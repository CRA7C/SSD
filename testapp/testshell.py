from testapp.command_parser import CommandParser
from testapp.constants import INVALID_COMMAND
from testapp.scripts import get_test_scripts, run_script
from my_logger import Logger

EXECUTE_VALID_WO_ARGS = 2
EXECUTE_VALID_WITH_ARGS = 1
EXECUTE_INVALID = 0


class TestShell:
    """
    TestShell 클래스는 명령어를 실행하고, 사전 정의된 명령어 또는 테스트 스크립트를 실행하는 기능을 제공합니다.

    """

    @staticmethod
    def execute(cmd: str) -> int:
        """
        주어진 명령어를 실행합니다.

        Args:
            cmd (str): 실행할 명령어

        Returns:
            int: 명령어 실행 결과 코드
                 - EXECUTE_VALID_WO_ARGS (2): 인자가 없는 유효한 명령어
                 - EXECUTE_VALID_WITH_ARGS (1): 인자가 있는 유효한 명령어
                 - EXECUTE_INVALID (0): 유효하지 않은 명령어
        """
        cmd_option = cmd.split()[0]
        if CommandParser.is_predefined_command(cmd_option):
            cmd_option, cmd_args = CommandParser.parse_args(cmd)
            if not CommandParser.validate_command(cmd):
                # Logger().debug(INVALID_COMMAND)
                return EXECUTE_INVALID
            cmd_if = CommandParser.get_command(cmd_option)
            cmd_if.run(*cmd_args)
            return EXECUTE_VALID_WITH_ARGS if cmd_args else EXECUTE_VALID_WO_ARGS

        else:  # test script 중에 있으면 동작
            ts_dict = get_test_scripts()
            if cmd_option in ts_dict.keys():
                success = run_script(ts_dict[cmd_option])
                Logger().debug('PASS' if success else 'FAIL!')
                return success
        return EXECUTE_INVALID


def main():
    """
    TestShell의 메인 루프를 실행합니다.
    사용자가 명령어를 입력하고 이를 처리합니다.
    """
    while True:
        cmd = input("> ")
        if TestShell.execute(cmd) == EXECUTE_INVALID:
            Logger().debug(INVALID_COMMAND)
