import os
from pathlib import Path

NAND_FILE_PATH = Path(__file__).parent / 'nand.txt'


class NandDriver:
    """ NAND Driver
    nand.txt 파일 기반으로 read, write 기능을 수행한다.
    """

    def __init__(self):
        self.nand_file_path = NAND_FILE_PATH
        self.initiate_nand_file(self.nand_file_path)

    def initiate_nand_file(self, nand_file_path):
        if not os.path.exists(nand_file_path):
            with open(nand_file_path, 'w') as f:
                f.write('\n'.join(['0x00000000' for _ in range(100)]))

    def read(self, lba) -> int:
        with open(self.nand_file_path, 'r') as f:
            contents = f.read()
        for i, line in enumerate(contents.split('\n')):
            if i == lba:
                return int(line, 16)

    def write(self, lba, value):
        with open(self.nand_file_path, 'r') as f:
            contents = f.read()
        result = self.write_value(contents, lba, value)
        with open(self.nand_file_path, 'w') as f:
            f.write(result)

    def write_value(self, contents, lba, value):
        result = []
        for i, line in enumerate(contents.split('\n')):
            if i == lba:
                hex_str = "0x" + hex(value)[2:].upper().zfill(8)
                result.append(hex_str)
            else:
                result.append(line)
        return '\n'.join(result)
