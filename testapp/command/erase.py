from testapp.command.__interface import CommandInterface
from testapp.command.erase_common import request_erase
from testapp.constants import SSD_SIZE
from testapp.ssd_driver import SsdDriver
from testapp.util import is_valid_size, is_in_range_lba


class EraseCommand(CommandInterface):
    """
    Erase 클래스는 지정된 LBA 범위의 데이터를 삭제하는 명령어를 구현합니다.

    Attributes:
        driver (SsdDriver): SSD 드라이버 객체
    """
    required_args_cnt: int = 2

    def __init__(self):
        self.driver = SsdDriver()

    def run(self, lba: str, total_size: str):
        """
        지정된 LBA와 크기만큼 데이터를 삭제합니다.

        Args:
            lba (str): 시작 논리 블록 주소
            total_size (str): 삭제할 총 크기
        """
        erase_size = int(total_size)
        initial_lba = int(lba)
        target_lba = initial_lba + erase_size
        end_lba = SSD_SIZE if target_lba > SSD_SIZE else target_lba
        request_erase(self.driver, initial_lba, end_lba)

    @staticmethod
    def is_valid_args(*args) -> bool:
        """
        주어진 인자가 유효한지 확인합니다.

        Args:
            *args: 확인할 인자 (LBA와 크기)

        Returns:
            bool: 인자가 유효한 경우 True, 그렇지 않으면 False
        """
        n_lba = args[1]
        size = args[2]
        if not is_in_range_lba(n_lba):
            return False
        if not is_valid_size(size):
            return False
        return True
