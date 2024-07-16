import os
from pathlib import Path
from typing import Union

from ssd.common import convert_hex_to_str, LBA_SIZE

NAND_INITIAL_VALUE = '0x00000000'
NAND_FILE_PATH = Path(__file__).parent / 'nand.txt'


class NandDriver:
    """ NAND Driver
    nand.txt 파일 기반으로 read, write 기능을 수행한다.
    """
    def __init__(self, nand_file_path: Union[Path, str] = NAND_FILE_PATH):
        self.nand_file_path: Path = Path(nand_file_path)
        self.initialize()

    def initialize(self) -> None:
        # 만일 nand.txt 파일이 없으면, 초기화 된 파일 생성
        if not self.nand_file_path.exists():
            with open(self.nand_file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join([NAND_INITIAL_VALUE] * LBA_SIZE))

    def read(self, lba: int) -> int:
        with open(self.nand_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return int(lines[lba].strip(), 16)

    def write(self, lba: int, value: int) -> None:
        with open(self.nand_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        lines[lba] = convert_hex_to_str(value) + '\n'
        with open(self.nand_file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
