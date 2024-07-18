from testapp.command.__interface import CommandInterface
from testapp.ssd_driver import SsdDriver
from testapp.util import is_in_range_lba


class ReadCommand(CommandInterface):
    """
    Read 클래스는 지정된 LBA에서 데이터를 읽는 명령어를 구현합니다.

    Attributes:
        driver (SsdDriver): SSD 드라이버 객체
    """
    required_args_cnt: int = 1

    def __init__(self):
        super().__init__()
        self.driver = SsdDriver()

    def run(self, lba: str) -> str:
        """
        지정된 LBA에서 데이터를 읽습니다.

        Args:
            lba (str): 논리 블록 주소

        Returns:
            str: 읽은 데이터
        """
        ret = self.driver.read(lba)
        print(ret)  # shell 의 출력
        return ret  # test script 에서 이 값을 사용하기 위함.

    @staticmethod
    def is_valid_args(*args) -> bool:
        """
        주어진 인자가 유효한지 확인합니다.

        Returns:
            bool: 인자가 유효한 경우 True, 그렇지 않으면 False
        """
        n_lba = args[1]
        return True if is_in_range_lba(n_lba) else False
