from pathlib import Path
from typing import Union

from ssd.common import convert_hex_to_str, LBA_SIZE, LBA_UPPER_LIMIT

NAND_INITIAL_VALUE = '0x00000000'
NAND_FILE_PATH = Path(__file__).parent / 'nand.txt'


class NandDriver:
    """
    NandDriver 클래스는 nand.txt 파일을 기반으로 NAND 읽기, 쓰기 및 삭제 기능을 제공합니다.

    Attributes:
        nand_file_path (Path): NAND 파일 경로
    """

    def __init__(self, nand_file_path: Union[Path, str] = NAND_FILE_PATH):
        """
        NandDriver 클래스의 생성자. NAND 파일 경로를 설정하고 초기화합니다.

        Args:
            nand_file_path (Union[Path, str], optional): NAND 파일 경로. 기본값은 NAND_FILE_PATH.
        """
        self.nand_file_path: Path = Path(nand_file_path)
        self.initialize()

    def initialize(self) -> None:
        """
        만일 nand.txt 파일이 없으면, 초기화된 파일을 생성합니다.
        """
        if not self.nand_file_path.exists():
            with open(self.nand_file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join([NAND_INITIAL_VALUE] * LBA_SIZE))

    def read(self, lba: int) -> int:
        """
        주어진 LBA에서 값을 읽어 반환합니다.

        Args:
            lba (int): 논리 블록 주소

        Returns:
            int: 읽은 값 (정수 형식)
        """
        with open(self.nand_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return int(lines[lba].strip(), 16)

    def write(self, lba: int, value: int) -> None:
        """
        주어진 LBA에 값을 씁니다.

        Args:
            lba (int): 논리 블록 주소
            value (int): 쓸 값 (정수 형식)
        """
        with open(self.nand_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        lines[lba] = convert_hex_to_str(value) + '\n'
        with open(self.nand_file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    def erase(self, lba: int, n_value: int) -> None:
        """
        주어진 LBA부터 n_value 개의 블록을 삭제합니다.

        Args:
            lba (int): 논리 블록 주소
            n_value (int): 삭제할 블록 수
        """
        LAST_LBA = min(lba + n_value - 1, LBA_UPPER_LIMIT)
        with open(self.nand_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for idx_lba in range(lba, LAST_LBA +1):
            lines[idx_lba] = NAND_INITIAL_VALUE + '\n'
        with open(self.nand_file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
