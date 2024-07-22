from pathlib import Path
from typing import Final, Iterable

# LBA (Logical Block Address) 관련
SSD_START_LBA: Final[int] = 0
SSD_END_LBA: Final[int] = 99
SSD_SIZE: Final[int] = SSD_END_LBA - SSD_START_LBA + 1
SSD_LBA_RANGE: Final[Iterable[int]] = range(SSD_START_LBA, SSD_END_LBA + 1)

# SSD Value 관련
SSD_MIN_VALUE: Final[int] = 0x00000000
SSD_MAX_VALUE: Final[int] = 0xFFFFFFFF

INVALID_COMMAND = "INVALID COMMAND"

PROJECT_ROOT = Path(__file__).parent.resolve()
SCRIPTS_DIRECTORY = PROJECT_ROOT / 'scripts'

# LOGGER MAX BLOCK
MAX_BLOCK = 1000