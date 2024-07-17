from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver
from testapp.constants import SSD_LBA_RANGE


class FullRead(CommandInterface):
    """
    FullRead 클래스는 SSD의 모든 LBA에서 데이터를 읽는 명령어를 구현합니다.

    Attributes:
        driver (SsdDriver): SSD 드라이버 객체
    """
    def __init__(self):
        super().__init__()
        self.driver = SsdDriver()

    def run(self) -> list[str]:
        """
        SSD의 모든 LBA에서 데이터를 읽어 리스트로 반환합니다.

        Returns:
            list[str]: SSD의 모든 LBA에서 읽은 데이터 리스트
        """
        return [self.driver.read(addr) for addr in SSD_LBA_RANGE]

    @staticmethod
    def is_valid_args(*args) -> bool:
        """
        주어진 인자가 유효한지 확인합니다.
        """
        return True
