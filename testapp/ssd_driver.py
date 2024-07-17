import subprocess

from testapp.util import get_ssd_result, validate_ssd_command, BASE_DIR


class SsdDriver:
    """
    SSD Driver 클래스는 SSD를 Python 레벨에서 접근하여 제어할 수 있도록 해주는 드라이버입니다.
    - subprocess를 사용하여 SSD에 접근하도록 설계되었습니다.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def run_subprocess(command):
        """
        주어진 명령어를 서브프로세스로 실행합니다.

        Args:
            command (str): 실행할 명령어

        Returns:
            subprocess.CompletedProcess: 서브프로세스 실행 결과

        Raises:
            Exception: 명령어 실행 중 오류가 발생한 경우
        """
        validate_ssd_command(command)
        subprocess_cmd = f"python -m {command}"
        try:
            return subprocess.run(subprocess_cmd, shell=True, check=True, cwd=BASE_DIR,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error executing command: {e.stderr}")

    def read(self, lba: str | int) -> str:
        """
        주어진 LBA에서 데이터를 읽습니다.

        Args:
            lba (str | int): 논리 블록 주소

        Returns:
            str: 읽은 데이터
        """
        self.run_subprocess(f"ssd R {lba}")
        return get_ssd_result()

    def write(self, lba: str | int, value: str | int):
        """
        주어진 LBA에 데이터를 씁니다.

        Args:
            lba (str | int): 논리 블록 주소
            value (str | int): 쓸 데이터
        """
        if isinstance(value, int):
            value = f"0x{value:08X}"
        self.run_subprocess(f"ssd W {lba} {value}")

    def erase(self, lba: str | int, size: str | int):
        """
        주어진 LBA부터 주어진 크기만큼 데이터를 삭제합니다.

        Args:
            lba (str | int): 논리 블록 주소
            size (str | int): 삭제할 크기
        """
        self.run_subprocess(f"ssd E {lba} {size}")

    def flush(self):
        self.run_subprocess(f"ssd F")
