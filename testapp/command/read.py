from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver
from testapp.util import is_in_range_lba
from my_logger import Logger


class Read(CommandInterface):
    """
    Read 클래스는 지정된 LBA에서 데이터를 읽는 명령어를 구현합니다.

    Attributes:
        driver (SsdDriver): SSD 드라이버 객체
    """

    def __init__(self):
        super().__init__()
        self.driver = SsdDriver()

    def run(self, lba: str | int) -> str:
        """
        지정된 LBA에서 데이터를 읽습니다.
        읽어온 데이터를 화면에 출력합니다.

        Args:
            lba (str | int): 논리 블록 주소
        """
        read_value = self.driver.read(lba)
        Logger().info(read_value)
        return read_value

    @staticmethod
    def is_valid_args(*args) -> bool:
        """
        주어진 인자가 유효한지 확인합니다.

        Returns:
            bool: 인자가 유효한 경우 True, 그렇지 않으면 False
        """
        n_lba = args[1]
        return True if is_in_range_lba(n_lba) else False
