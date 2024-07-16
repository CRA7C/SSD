import sys
import io
from functools import wraps
from typing import Union
from pathlib import Path

from testapp.constants import SSD_MIN_VALUE, SSD_MAX_VALUE

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


def validate_ssd_command(command):
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


def validate_ssd_lba(lba: Union[str, int]):
    if not isinstance(lba, (str, int)):
        raise TypeError
    elif not 0 <= int(lba) < 100:
        raise ValueError


def validate_ssd_value(value: Union[str, int]):
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
