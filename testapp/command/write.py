from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver
from testapp.util import validate_ssd_lba, validate_ssd_value


class WriteCommand(CommandInterface):
    """
    Write 클래스는 지정된 LBA에 데이터를 쓰는 명령어를 구현합니다.

    Attributes:
        driver (SsdDriver): SSD 드라이버 객체
    """
    required_args_cnt: int = 2

    def __init__(self):
        super().__init__()
        self.driver = SsdDriver()

    def run(self, lba: str | int, value: str | int) -> None:
        """
        지정된 LBA에 데이터를 씁니다.

        Args:
            lba (str | int): 논리 블록 주소
            value (str | int): 쓸 데이터 (16진수 문자열)
        """
        self.driver.write(lba, value)

    @staticmethod
    def is_valid_args(*args) -> bool:
        """
        주어진 인자가 유효한지 확인합니다.

        Returns:
            bool: 인자가 유효한 경우 True, 그렇지 않으면 False
        """
        n_lba = args[1]
        value = args[2]
        validate_ssd_lba(n_lba)
        validate_ssd_value(value)
        return True
