from pathlib import Path

RESULT_FILE_PATH = Path(__file__).parent / 'result.txt'


class ResultManager:

    def __init__(self):
        self.result_file_path: Path = RESULT_FILE_PATH
        self.initialize()

    def initialize(self):
        # 만일 result.txt 파일이 없으면, 초기화 된 파일 생성
        if not self.result_file_path.exists():
            with open(self.result_file_path, 'w', encoding='utf-8') as f:
                f.write("0x00000000")

    def write(self, text):
        with open(self.result_file_path, 'w', encoding='utf-8') as f:
            f.write(text)
