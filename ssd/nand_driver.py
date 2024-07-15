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
        with open(self.nand_file_path, 'w') as f:
            f.write(contents)
