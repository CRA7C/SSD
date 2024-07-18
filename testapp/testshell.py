from testapp.command.command_factory import (CommandFactory, is_predefined_command_name,
                                             validate_command, parse_cmd_args)
from testapp.constants import INVALID_COMMAND
from testapp.scripts import get_test_scripts, run_script
from my_logger import Logger

EXECUTE_VALID_WO_ARGS = 2
EXECUTE_VALID_WITH_ARGS = 1
EXECUTE_INVALID = 0
EXECUTE_EMPTY = -1

logger = Logger()


class TestShell:
    """
    TestShell 클래스는 명령어를 실행하고, 사전 정의된 명령어 또는 테스트 스크립트를 실행하는 기능을 제공합니다.
    """

    def execute(self, cmd: str) -> int:
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
        if len(cmd) == 0:
            return EXECUTE_EMPTY
        cmd = cmd.strip()

        cmd_option = cmd.split()[0]

        if is_predefined_command_name(cmd_option):
            if not validate_command(cmd):
                return EXECUTE_INVALID
            cmd_option, cmd_args = parse_cmd_args(cmd)
            cmd_obj = CommandFactory.get_command_instance(cmd_option)
            cmd_obj.run(*cmd_args)
            return EXECUTE_VALID_WITH_ARGS if cmd_args else EXECUTE_VALID_WO_ARGS

        else:  # test script 중에 있으면 동작
            ts_dict = get_test_scripts()  # UpperCamelCase
            ts_dict.update({k.lower(): v for k, v in ts_dict.items()})  # lower case 도 포함
            if cmd_option in ts_dict.keys():
                success = run_script(ts_dict[cmd_option])
                logger.debug('PASS' if success else 'FAIL!')
                return success
        return EXECUTE_INVALID


def main():
    """
    TestShell의 메인 루프를 실행합니다.
    사용자가 명령어를 입력하고 이를 처리합니다.
    """
    ts = TestShell()
    while True:
        cmd = input("> ")
        if ts.execute(cmd) == EXECUTE_INVALID:
            logger.info(INVALID_COMMAND)
