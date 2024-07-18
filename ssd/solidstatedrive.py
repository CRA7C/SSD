from ssd.common import convert_hex_to_str
from ssd.nand_driver import NandDriver
from ssd.result_manager import ResultManager


class SolidStateDrive:
    """
    SolidStateDrive 클래스는 가상 SSD의 읽기, 쓰기, 삭제 기능을 제공합니다.

    Attributes:
        nand_driver (NandDriver): NAND 드라이버 객체
        result_manager (ResultManager): 결과 관리 객체
    """
    def __init__(self):
        self.nand_driver = NandDriver()
        self.result_manager = ResultManager()

    def write(self, lba: int, value):
        """
        주어진 LBA에 값을 씁니다.

        Args:
            lba (int): 논리 블록 주소
            value (str): 쓸 값 (16진수 문자열 형식)
        """
        self.nand_driver.write(lba, value)

    def read(self, lba: int):
        """
        주어진 LBA에서 값을 읽고 결과를 기록합니다.

        Args:
            lba (int): 논리 블록 주소
        """
        result = self.nand_driver.read(lba)
        self.result_manager.write(convert_hex_to_str(result))

    def read_fast(self, value: int):
        """
        값을 빠르게 읽고 결과를 기록합니다.

        Args:
            value (int): 읽을 값 (16진수)
        """
        self.result_manager.write(convert_hex_to_str(value))

    def erase(self, lba: int, n_value: int):
        """
        주어진 LBA부터 n_value 개의 블록을 삭제합니다.

        Args:
            lba (int): 논리 블록 주소
            n_value (int): 삭제할 블록 수
        """
        self.nand_driver.erase(lba, n_value)
