class Command:
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

    def get_key(self):
        """
        명령 키를 반환합니다.

        Returns:
            tuple: 명령 키 (옵션, 시작 LBA, 끝 LBA)
        """
        return (self.option, self.lba, self.lba + 1)


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

    def get_key(self):
        """
        명령 키를 반환합니다.

        Returns:
            tuple: 명령 키 (옵션, 시작 LBA, 끝 LBA)
        """
        return (self.option, self.lba, self.lba + self.size)


class CommandFactory:
    """
    명령어 생성 클래스입니다.
    주어진 명령 인자 리스트를 통해 적절한 명령어 객체를 생성합니다.
    """
    @staticmethod
    def parse_command(command_list):
        """
        주어진 명령 인자 리스트를 통해 적절한 명령어 객체를 생성합니다.

        Args:
            command_list (list): 명령 인자 리스트

        Returns:
            Command: 생성된 명령어 객체
        """
        name = command_list[0]
        if name == 'R':
            return ReadCommand(command_list)
        elif name == 'W':
            return WriteCommand(command_list)
        elif name == 'E':
            return EraseCommand(command_list)
        else:
            return Command(command_list)
