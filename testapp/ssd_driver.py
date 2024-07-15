class SsdDriver:
    """ SSD Driver
    - ssd 를 python level에서 접근하여 쓸 수 있게 해주는 드라이버
    - subprocess 를 사용하여 ssd 에 접근하도록 설계
    """

    def _run(self, command):
        pass

    def read(self, lba) -> int:
        pass

    def write(self, lba, value):
        pass
