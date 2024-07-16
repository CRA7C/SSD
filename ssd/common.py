from typing import Final

LBA_LOWER_LIMIT: Final[int] = 0
LBA_UPPER_LIMIT: Final[int] = 99
LBA_SIZE: Final[int] = LBA_UPPER_LIMIT - LBA_LOWER_LIMIT + 1


def convert_hex_to_str(value):
    return f"0x{value:08X}"
