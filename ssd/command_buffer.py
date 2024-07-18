from pathlib import Path
from typing import List, Tuple, Set

from ssd.command import CommandFactory, Command, ReadCommand

BUFFER_FILE_PATH = Path(__file__).parent / 'buffer.txt'


class CommandBuffer:
    """
    CommandBuffer 클래스는 명령어를 버퍼에 저장하고 최적화하는 기능을 제공합니다.
    명령어는 buffer.txt 파일에 저장되며, 필요한 경우 버퍼를 비울 수 있습니다.

    Attributes:
        buffer_file_path (Path): 버퍼 파일 경로
        buffer (list): 명령어를 저장하는 리스트
    """

    def __init__(self):
        """
        CommandBuffer 클래스의 생성자. 버퍼 파일 경로를 설정하고 초기화합니다.
        """
        self.buffer_file_path: Path = Path(BUFFER_FILE_PATH)
        self.buffer: List[Command] = []
        self.initialize()

    def initialize(self):
        """
        버퍼 파일을 초기화합니다. 만일 buffer.txt 파일이 없으면, 초기화된 파일을 생성합니다.
        """
        if not self.buffer_file_path.exists():
            with open(self.buffer_file_path, 'w', encoding='utf-8'):
                pass
        else:
            self.load_buffer()

    def load_buffer(self):
        """
        버퍼 파일에서 명령어를 읽어와 버퍼에 저장합니다.
        """
        with open(self.buffer_file_path, 'r') as f:
            self.buffer = [CommandFactory().parse_command(line.split()) for line in f.readlines()]

    def save_buffer(self):
        """
        버퍼 파일에 현재 버퍼의 명령어를 저장합니다.
        """
        with open(self.buffer_file_path, 'w') as f:
            f.write(self.get_saved_data())

    def get_saved_data(self) -> str:
        """
        버퍼에 저장된 명령어 데이터를 문자열 형식으로 반환합니다.

        Returns:
            str: 버퍼에 저장된 명령어 문자열
        """
        txt = []
        for data in self.buffer:
            txt.append(' '.join(data.get_value()) + '\n')
        return ''.join(txt)

    def push_command(self, command: Command):
        """
        명령어를 버퍼에 추가하고 최적화합니다.

        Args:
            command: 버퍼에 추가할 명령어
        """
        self.buffer.append(command)
        self.optimize()
        self.save_buffer()

    def pop(self):
        """
        버퍼에서 명령어를 제거하고 반환합니다.

        Returns:
            명령어: 제거된 명령어
        """
        value = self.buffer.pop()
        self.save_buffer()
        return value

    def is_able_to_fast_read(self, cmd: Command) -> bool:
        """
        빠른 읽기가 가능한지 확인합니다.

        Args:
            cmd: 확인할 명령어

        Returns:
            bool: 빠른 읽기가 가능한 경우 True, 그렇지 않으면 False
        """
        for command in self.buffer[::-1]:
            if command.option == 'W' and command.lba == cmd.lba:
                return True
            elif command.option == 'E' and command.lba <= cmd.lba < command.lba + command.size:
                return True
        return False

    def get_read_fast(self, cmd: ReadCommand) -> int:
        """
        버퍼에서 빠른 읽기 값을 반환합니다.

        Args:
            cmd: 읽기 명령어

        Returns:
            int: 읽은 값
        """
        for command in self.buffer[::-1]:
            if command.option == 'W' and command.lba == cmd.lba:
                return command.value
            elif command.option == 'E' and command.lba <= cmd.lba < command.lba + command.size:
                return 0x00000000

    def flush(self) -> List[Command]:
        """
        버퍼를 비우고 모든 명령어를 반환합니다.

        Returns:
            list: 비워진 버퍼의 모든 명령어
        """
        cmd_list = [value for value in self.buffer]
        self.buffer.clear()
        self.save_buffer()
        return cmd_list

    def optimize(self):
        """
        버퍼 내 명령어를 최적화합니다.
        """
        write_commands = set()
        erase_commands = set()
        for command in self.buffer[::-1]:
            key = command.get_key()
            if command.option == 'W':
                if key in write_commands or self.merge_write_with_erase(erase_commands, key):
                    self.buffer.remove(command)
                else:
                    write_commands.add(key)
            elif command.option == 'E':
                if self.merge_write_with_erase(erase_commands, key):
                    self.buffer.remove(command)
                else:
                    erase_commands.add(key)

        self.save_buffer()

    @staticmethod
    def merge_write_with_erase(erase_commands: Set[Tuple[str, int, int]], key: Tuple[str, int, int]):
        """
        쓰기 명령어와 삭제 명령어를 병합합니다.

        Args:
            erase_commands (set): 삭제 명령어 집합
            key (tuple): 쓰기 명령어의 키

        Returns:
            bool: 병합 가능한 경우 True, 그렇지 않으면 False
        """
        for erase in erase_commands:
            if erase[1] <= key[1] and key[2] <= erase[2]:
                return True
        return False

    def need_flush(self) -> bool:
        """
        버퍼를 비울 필요가 있는지 확인합니다.

        Returns:
            bool: 버퍼를 비울 필요가 있는 경우 True, 그렇지 않으면 False
        """
        return len(self.buffer) > 10
