import os.path
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


def get_ssd_result() -> str:
    file_path = BASE_DIR / 'ssd' / 'result.txt'
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    raise Exception(f"Can't read {os.path.basename()}.")


def run_subprocess(args_str):
    command = f"python {args_str}"
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=BASE_DIR,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error executing command: {e.stderr}")
    return result.stdout


if __name__ == '__main__':
    # print(get_ssd_result())
    run_subprocess('ssd W 3 0x1298CDEF')
    ret = run_subprocess('ssd R 3')
    print(ret)
