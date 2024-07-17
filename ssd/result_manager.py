from pathlib import Path

RESULT_FILE_PATH = Path(__file__).parent / 'result.txt'


class ResultManager:
    """
    ResultManager 클래스는 result.txt 파일을 관리하는 기능을 제공합니다.

    Attributes:
        result_file_path (Path): 결과 파일 경로
    """

    def __init__(self):
        """
        ResultManager 클래스의 생성자. 결과 파일 경로를 설정하고 초기화합니다.
        """
        self.result_file_path: Path = RESULT_FILE_PATH
        self.initialize()

    def initialize(self):
        """
        결과 파일을 초기화합니다. 만일 result.txt 파일이 없으면, 초기화된 파일을 생성합니다.
        """
        if not self.result_file_path.exists():
            with open(self.result_file_path, 'w', encoding='utf-8') as f:
                f.write("0x00000000")

    def write(self, text):
        """
        결과 파일에 텍스트를 씁니다.

        Args:
            text (str): 결과 파일에 쓸 텍스트
        """
        with open(self.result_file_path, 'w', encoding='utf-8') as f:
            f.write(text)
