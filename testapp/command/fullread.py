from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver
from testapp.constants import SSD_LBA_RANGE


class FullReadCommand(CommandInterface):
    """
    FullRead 클래스는 SSD의 모든 LBA에서 데이터를 읽는 명령어를 구현합니다.

    Attributes:
        driver (SsdDriver): SSD 드라이버 객체
    """
    required_args_cnt: int = 0

    def __init__(self):
        super().__init__()
        self.driver = SsdDriver()

    def run(self) -> list[str]:
        """
        SSD의 모든 LBA에서 데이터를 읽어 리스트로 반환합니다.

        Returns:
            list[str]: SSD의 모든 LBA에서 읽은 데이터 리스트
        """
        ret = [self.driver.read(addr) for addr in SSD_LBA_RANGE]
        for i, value in enumerate(ret):
            print(f"LBA: {i:02}, value: {value}")  # print 는 shell 의 출력으로 사용
        return ret  # return 값은 test script 에서 사용

    @staticmethod
    def is_valid_args(*args) -> bool:
        """
        주어진 인자가 유효한지 확인합니다.
        """
        return True
