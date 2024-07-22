from testapp.command.__interface import CommandInterface
from testapp.command.erase_common import request_erase
from testapp.ssd_driver import SsdDriver
from testapp.util import validate_ssd_lba, validate_ssd_end_lba


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

        start_lba = args[1]
        end_lba = args[2]
        validate_ssd_lba(start_lba)
        validate_ssd_end_lba(end_lba)
        if int(start_lba) >= int(end_lba):
            raise ValueError("end LBA는 start LBA보다 커야합니다.")
        return True
