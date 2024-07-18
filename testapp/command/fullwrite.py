from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver
from testapp.constants import SSD_LBA_RANGE
from testapp.util import is_valid_hex


class FullWriteCommand(CommandInterface):
    """
    FullWrite 클래스는 SSD의 모든 LBA에 동일한 값을 쓰는 명령어를 구현합니다.

    Attributes:
        driver (SsdDriver): SSD 드라이버 객체
    """
    required_args_cnt: int = 1

    def __init__(self):
        super().__init__()
        self.driver = SsdDriver()

    def run(self, value: str) -> None:
        """
        SSD의 모든 LBA에 값을 씁니다.

        Args:
            value (str): 쓸 값 (16진수 문자열)
        """
        for i in SSD_LBA_RANGE:
            self.driver.write(i, value)

    @staticmethod
    def is_valid_args(*args) -> bool:
        """
        주어진 인자가 유효한지 확인합니다.

        Returns:
            bool: 인자가 유효한 경우 True, 그렇지 않으면 False
        """
        value = args[1]
        return True if is_valid_hex(value) else False
