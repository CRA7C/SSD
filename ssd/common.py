import re
from typing import Final

LBA_LOWER_LIMIT: Final[int] = 0
LBA_UPPER_LIMIT: Final[int] = 99
LBA_SIZE: Final[int] = LBA_UPPER_LIMIT - LBA_LOWER_LIMIT + 1

SSD_MIN_VALUE: Final[int] = 0x00000000
SSD_MAX_VALUE: Final[int] = 0xFFFFFFFF


def convert_hex_to_str(value: int):
    """
    정수 값을 8자리 16진수 문자열로 변환합니다.

    Args:
        value (int): 변환할 정수 값

    Returns:
        str: 16진수 문자열 (예: '0x00000000')
    """
    return f"0x{value:08X}"


def is_valid_hex(s: str):
    """
    주어진 문자열이 유효한 16진수 형식인지 확인합니다.

    Args:
        s (str): 검사할 문자열

    Returns:
        bool: 유효한 16진수 형식이면 True, 그렇지 않으면 False
    """
    if re.fullmatch(r"0x[0-9A-Fa-f]{8}", s):
        try:
            num = int(s, 16)
            return SSD_MIN_VALUE <= num <= SSD_MAX_VALUE
        except ValueError:
            return False
    return False
