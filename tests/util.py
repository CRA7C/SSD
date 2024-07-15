import os.path
from pathlib import Path


def get_ssd_result() -> str:
    file_path = Path(__file__).parent.parent / 'ssd' / 'result.txt'
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    raise Exception(f"Can't read {os.path.basename()}.")


if __name__ == '__main__':
    print(get_ssd_result())
