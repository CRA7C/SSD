from testapp.command.__interface import CommandInterface
from testapp.scripts import get_test_scripts

TESTAPP_HELP = r"""
Usage:
  <command> [options]

Commands:
  write             SSD 데이터 쓰기
  read              SSD 데이터 읽기
  exit              TestShellApplication 종료
  help              Help 보기
  fullwrite         SSD 데이터를 특정 값으로 일괄 쓰기
  fullread          SSD 데이터 전체 읽기
  erase             SSD 데이터 지우기 (LBA ~ LBA + SIZE)
  erase_range       SSD 데이터 지우기 (Start LBA ~ End LBA)
  flush             Command Buffer에 있는 모든 명령어들을 수행하여 Buffer를 비움
  cls               Clear Screen
"""


class HelpCommand(CommandInterface):
    """
    Help 클래스는 사용 가능한 명령어와 옵션을 출력하는 명령어를 구현합니다.
    """
    required_args_cnt: int = 0

    def run(self):
        """
        사용 가능한 명령어와 옵션을 출력합니다.
        """
        print(TESTAPP_HELP)
        test_scripts_dict = get_test_scripts()
        if test_scripts_dict:
            print("Test Scripts:")
            for key in test_scripts_dict.keys():
                print(f"  {key}")

    @staticmethod
    def is_valid_args(*args) -> bool:
        """
        주어진 인자가 유효한지 확인합니다.
        """
        return True
