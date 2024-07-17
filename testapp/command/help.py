from testapp.command.__interface import CommandInterface

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
"""


class Help(CommandInterface):
    def run(self, *args, **kwarg):
        print(TESTAPP_HELP)

    @staticmethod
    def is_valid_args(self, *args):
        return True
