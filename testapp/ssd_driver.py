import subprocess

from testapp.util import get_ssd_result, validate_ssd_command, BASE_DIR


class SsdDriver:
    """ SSD Driver
    - ssd 를 python level에서 접근하여 쓸 수 있게 해주는 드라이버
    - subprocess 를 사용하여 ssd 에 접근하도록 설계
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def run_subprocess(command):
        validate_ssd_command(command)
        subprocess_cmd = f"python -m {command}"
        try:
            return subprocess.run(subprocess_cmd, shell=True, check=True, cwd=BASE_DIR,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error executing command: {e.stderr}")

    def read(self, lba: str | int) -> str:
        self.run_subprocess(f"ssd R {lba}")
        return get_ssd_result()

    def write(self, lba: str | int, value: str | int):
        if isinstance(value, int):
            value = f"0x{value:08X}"
        self.run_subprocess(f"ssd W {lba} {value}")
