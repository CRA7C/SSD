from testapp.ssd_driver import SsdDriver

MAXIMUM_ERASE_SIZE_AT_ONCE = 10


def request_erase(driver: SsdDriver, start_lba: int, end_lba: int):
    """
    지정된 범위의 LBA를 최대 삭제 크기 단위로 나누어 삭제 요청을 보냅니다.

    Args:
        driver (SsdDriver): SSD 드라이버 객체
        start_lba (int): 삭제를 시작할 LBA
        end_lba (int): 삭제를 종료할 LBA (포함되지 않음)
    """
    remain_erase_size = end_lba - start_lba
    for lba in range(start_lba, end_lba, MAXIMUM_ERASE_SIZE_AT_ONCE):
        if remain_erase_size > MAXIMUM_ERASE_SIZE_AT_ONCE:
            size = MAXIMUM_ERASE_SIZE_AT_ONCE
            remain_erase_size -= size
        else:
            size = remain_erase_size
            remain_erase_size = 0
        driver.erase(lba, size)
