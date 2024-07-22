from testapp.command.__interface import CommandInterface
from testapp.command.erase_common import request_erase
from testapp.ssd_driver import SsdDriver
from testapp.util import is_in_range_lba


class EraseRangeCommand(CommandInterface):
    """
    EraseRange 클래스는 지정된 LBA 범위의 데이터를 삭제하는 명령어를 구현합니다.

    Attributes:
        driver (SsdDriver): SSD 드라이버 객체
    """
    required_args_cnt: int = 2

    def __init__(self):
        self.driver = SsdDriver()

    def run(self, start_lba: str, end_lba: str):
        """
        지정된 시작 LBA와 끝 LBA 사이의 데이터를 삭제합니다.

        Args:
            start_lba (str): 시작 논리 블록 주소
            end_lba (str): 끝 논리 블록 주소
        """
        request_erase(self.driver, int(start_lba), int(end_lba))

    @staticmethod
    def is_valid_args(*args) -> bool:
        """
        주어진 인자가 유효한지 확인합니다.

        Returns:
            bool: 인자가 유효한 경우 True, 그렇지 않으면 False
        """
        if not (args[1].isdigit() and args[2].isdigit()):
            return False
        start_lba = int(args[1])
        end_lba = int(args[2])

        if not (is_in_range_lba(str(start_lba)) and is_in_range_lba(str(end_lba-1))):
            return False
        if start_lba >= end_lba:
            return False
        return True
