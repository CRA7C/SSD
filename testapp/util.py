import io
import re
import sys
from functools import wraps
from pathlib import Path
from typing import Union

from testapp.constants import SSD_MIN_VALUE, SSD_MAX_VALUE, SSD_START_LBA, SSD_END_LBA

RESULT_FILE = "result.txt"
READ_COMMAND = "R"
WRITE_COMMAND = "W"
SSD_COMMAND = "ssd"
SSD_MODULE = "ssd"

BASE_DIR = Path(__file__).parent.parent


def get_ssd_result() -> str:
    file_path = BASE_DIR / SSD_MODULE / RESULT_FILE
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def validate_ssd_command(command: str) -> None:
    if not isinstance(command, str):
        raise TypeError
    args = command.split(" ")
    if args[0] != SSD_COMMAND:
        raise ValueError(f"Applied wrong command: {command}")
    op = args[1]
    if op == WRITE_COMMAND and len(args) == 4:
        validate_ssd_lba(args[2])
        validate_ssd_value(args[3])
    elif op == READ_COMMAND and len(args) == 3:
        validate_ssd_lba(args[2])
    else:
        raise ValueError(f"Applied wrong command: {command}")


def validate_ssd_lba(lba: Union[str, int]) -> None:
    if not isinstance(lba, (str, int)):
        raise TypeError
    elif not 0 <= int(lba) < 100:
        raise ValueError


def validate_ssd_value(value: Union[str, int]) -> None:
    if not isinstance(value, (str, int)):
        raise TypeError
    elif isinstance(value, str):
        if not value.startswith("0x"):
            raise ValueError
        try:
            value = int(value, 16)  # 16 진수 to
        except:  # noqa
            raise ValueError()
    if not SSD_MIN_VALUE <= value <= SSD_MAX_VALUE:
        raise ValueError


def capture_output(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        output = io.StringIO()
        sys.stdout = output
        try:
            func(*args, **kwargs)
        finally:
            sys.stdout = sys.__stdout__
        captured_output = output.getvalue()
        return captured_output

    return wrapper


def is_in_range_lba(lba: str) -> bool:
    try:
        num = int(lba)
        return SSD_START_LBA <= num <= SSD_END_LBA
    except ValueError:
        return False


def is_valid_hex(s: str) -> bool:
    # 정규식으로 형식을 먼저 확인
    if re.fullmatch(r"0x[0-9A-Fa-f]{8}", s):
        try:
            # 16진수로 변환하여 범위를 확인
            num = int(s, 16)
            return SSD_MIN_VALUE <= num <= SSD_MAX_VALUE
        except ValueError:
            return False
    return False
  
  
def is_valid_size(size: str) -> bool:
    try:
        num = int(size)
        return 1 <= num
    except ValueError:
        return False
