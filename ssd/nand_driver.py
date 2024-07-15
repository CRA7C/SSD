class NandDriver:
    """ NAND Driver
    nand.txt 파일 기반으로 read, write 기능을 수행한다.
    """

    def __init__(self):
        self.nand_file_path = None

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
