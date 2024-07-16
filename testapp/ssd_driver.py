from testapp.util import *  # noqa


class SsdDriver:
    """ SSD Driver
    - ssd 를 python level에서 접근하여 쓸 수 있게 해주는 드라이버
    - subprocess 를 사용하여 ssd 에 접근하도록 설계
    """

    @staticmethod
    def run_subprocess(command):
        validate_ssd_command(command)
        subprocess_cmd = f"python {command}"
        try:
            return subprocess.run(subprocess_cmd, shell=True, check=True, cwd=BASE_DIR,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error executing command: {e.stderr}")

    def read(self, lba: int) -> int:
        result = self.run_subprocess(f"ssd R {lba}")
        return result.stdout

    def write(self, lba: int, value: int):
        self.run_subprocess(f"ssd W {lba} 0x{value:08X}")
