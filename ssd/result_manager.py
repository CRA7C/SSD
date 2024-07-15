from pathlib import Path

RESULT_FILE_PATH = Path(__file__).parent / 'result.txt'


class ResultManager:

    def __init__(self):
        self.result_file_path = RESULT_FILE_PATH

    def write(self, text):
        with open(self.result_file_path, 'w') as f:
            f.write(text)
