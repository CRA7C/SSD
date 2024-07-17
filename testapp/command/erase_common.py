from testapp.ssd_driver import SsdDriver

MAXIMUM_ERASE_SIZE_AT_ONCE = 10


def request_erase(driver: SsdDriver, start_lba: int, end_lba: int):
    remain_erase_size = end_lba - start_lba
    for lba in range(start_lba, end_lba, MAXIMUM_ERASE_SIZE_AT_ONCE):
        if remain_erase_size > MAXIMUM_ERASE_SIZE_AT_ONCE:
            size = MAXIMUM_ERASE_SIZE_AT_ONCE
            remain_erase_size -= size
        else:
            size = remain_erase_size
            remain_erase_size = 0
        driver.erase(lba, size)
