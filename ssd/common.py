import re
from typing import Final

LBA_LOWER_LIMIT: Final[int] = 0
LBA_UPPER_LIMIT: Final[int] = 99
LBA_SIZE: Final[int] = LBA_UPPER_LIMIT - LBA_LOWER_LIMIT + 1

SSD_MIN_VALUE: Final[int] = 0x00000000
SSD_MAX_VALUE: Final[int] = 0xFFFFFFFF


def convert_hex_to_str(value):
    return f"0x{value:08X}"


def is_valid_hex(s: str):
    if re.fullmatch(r"0x[0-9A-Fa-f]{8}", s):
        try:
            num = int(s, 16)
            return SSD_MIN_VALUE <= num <= SSD_MAX_VALUE
        except ValueError:
            return False
    return False
