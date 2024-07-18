from abc import ABC, abstractmethod
from ssd.common import LBA_LOWER_LIMIT, LBA_UPPER_LIMIT, is_valid_hex
from ssd.common import ERASE_SIZE_LOWER_LIMIT, ERASE_SIZE_UPPER_LIMIT


class Command(ABC):
    """
    기본 명령어 클래스입니다.

    Attributes:
        option (str): 명령 옵션
        args (list): 명령 인자 리스트
    """

    def __init__(self, args):
        """
        Command 클래스의 생성자. 명령 옵션과 인자를 설정합니다.

        Args:
            args (list): 명령 인자 리스트
        """
        self.option = args[0]
        self.args = args
        self.validate_command()

    @abstractmethod
    def validate_command(self):
        pass

    def get_value(self):
        """
        명령 인자를 반환합니다.

        Returns:
            list: 명령 인자 리스트
        """
        return self.args


class ReadCommand(Command):
    """
    읽기 명령어 클래스입니다.

    Attributes:
        lba (int): 논리 블록 주소
    """

    def __init__(self, args):
        """
        ReadCommand 클래스의 생성자. 논리 블록 주소를 설정합니다.

        Args:
            args (list): 명령 인자 리스트
        """
        super().__init__(args)
        self.lba = int(args[1])

    def validate_command(self):
        if len(self.args) != 2:
            raise ValueError("명령을 수행하기 위한 인자가 부족합니다. ex) ssd R 20")

        if not self.args[1].isdigit():
            raise ValueError('LBA는 숫자여야합니다.')
        if not LBA_LOWER_LIMIT <= int(self.args[1]) <= LBA_UPPER_LIMIT:
            raise ValueError(f'LBA는 {LBA_LOWER_LIMIT} ~ {LBA_UPPER_LIMIT} 여야합니다.')

        return True


class WriteCommand(Command):
    """
    쓰기 명령어 클래스입니다.

    Attributes:
        lba (int): 논리 블록 주소
        value (int): 쓸 값 (16진수 형식)
    """

    def __init__(self, args):
        """
        WriteCommand 클래스의 생성자. 논리 블록 주소와 쓸 값을 설정합니다.

        Args:
            args (list): 명령 인자 리스트
        """
        super().__init__(args)
        self.lba = int(args[1])
        self.value = int(args[2], 16)

    def validate_command(self):
        if len(self.args) != 3:
            raise ValueError("명령을 수행하기 위한 인자가 부족합니다. ex) ssd W 20 0x1234ABCD")

        if not self.args[1].isdigit():
            raise ValueError('LBA는 숫자여야합니다.')

        if not LBA_LOWER_LIMIT <= int(self.args[1]) <= LBA_UPPER_LIMIT:
            raise ValueError(f'LBA는 {LBA_LOWER_LIMIT} ~ {LBA_UPPER_LIMIT} 여야합니다.')

        if not is_valid_hex(self.args[2]):
            raise ValueError('value는 0x00000000 형식이여야 합니다.')

        return True

    def get_key(self):
        """
        명령 키를 반환합니다.

        Returns:
            tuple: 명령 키 (옵션, 시작 LBA, 끝 LBA)
        """
        return self.option, self.lba, self.lba + 1


class EraseCommand(Command):
    """
    삭제 명령어 클래스입니다.

    Attributes:
        lba (int): 논리 블록 주소
        size (int): 삭제할 블록 수
    """

    def __init__(self, args):
        """
        EraseCommand 클래스의 생성자. 논리 블록 주소와 삭제할 블록 수를 설정합니다.

        Args:
            args (list): 명령 인자 리스트
        """
        super().__init__(args)
        self.lba = int(args[1])
        self.size = int(args[2])

    def validate_command(self):
        if len(self.args) != 3:
            raise ValueError("명령을 수행하기 위한 인자가 부족합니다. ex) ssd E 20 4")

        if not self.args[1].isdigit():
            raise ValueError('LBA는 숫자여야합니다.')

        if not self.args[2].isdigit():
            raise ValueError('SIZE는 숫자여야합니다.')

        if not LBA_LOWER_LIMIT <= int(self.args[1]) <= LBA_UPPER_LIMIT:
            raise ValueError(f'LBA는 {LBA_LOWER_LIMIT} ~ {LBA_UPPER_LIMIT} 여야합니다.')

        if not ERASE_SIZE_LOWER_LIMIT <= int(self.args[2]) <= ERASE_SIZE_UPPER_LIMIT:
            raise ValueError(f"SIZE는 {ERASE_SIZE_LOWER_LIMIT} ~ {ERASE_SIZE_UPPER_LIMIT} 여야합니다.")

        return True

    def get_key(self):
        """
        명령 키를 반환합니다.

        Returns:
            tuple: 명령 키 (옵션, 시작 LBA, 끝 LBA)
        """
        return self.option, self.lba, self.lba + self.size


class FlushCommand(Command):
    """
    명령어 Buffer를 비우는 명령어 클래스입니다.

    Attributes:
        -
    """

    def __init__(self, args):
        """
        FlushCommand 클래스의 생성자. 논리 블록 주소와 삭제할 블록 수를 설정합니다.

        Args:
            args (list): 명령 인자 리스트
        """
        super().__init__(args)

    def validate_command(self):
        if len(self.args) != 1:
            raise ValueError("명령을 수행하기 위한 인자가 부족합니다. ex) ssd F")
        return True


class CommandFactory:
    """
    명령어 생성 클래스입니다.
    주어진 명령 인자 리스트를 통해 적절한 명령어 객체를 생성합니다.
    """

    @staticmethod
    def parse_command(arg_list: list) -> ReadCommand | WriteCommand | EraseCommand | FlushCommand:
        """
        주어진 명령 인자 리스트를 통해 적절한 명령어 객체를 생성합니다.

        Args:
            arg_list (list): 명령 인자 리스트

        Returns:
            Command: 생성된 명령어 객체
        """
        name = arg_list[0]
        if name == 'R':
            return ReadCommand(arg_list)
        elif name == 'W':
            return WriteCommand(arg_list)
        elif name == 'E':
            return EraseCommand(arg_list)
        elif name == 'F':
            return FlushCommand(arg_list)
        else:
            raise ValueError('R, W, E, F 중 하나를 사용해주세요.(대문자)')
