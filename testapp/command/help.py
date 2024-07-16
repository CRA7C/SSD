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
"""

class Help(CommandInterface):
    def run(self, *args, **kwarg):
        print(TESTAPP_HELP)
