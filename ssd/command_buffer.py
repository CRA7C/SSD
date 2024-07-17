from pathlib import Path
from collections import OrderedDict

BUFFER_FILE_PATH = Path(__file__).parent / 'buffer.txt'


class CommandBuffer:
    def __init__(self):
        self.buffer_file_path: Path = Path(BUFFER_FILE_PATH)
        self.buffer = OrderedDict()
        self.initialize()

    def initialize(self):
        # 만일 buffer.txt 파일이 없으면, 초기화 된 파일 생성
        if not self.buffer_file_path.exists():
            with open(self.buffer_file_path, 'w', encoding='utf-8') as f:
                pass
        else:
            self.load_buffer()

    def load_buffer(self):
        with open(self.buffer_file_path, 'r') as f:
            lines = [(tuple(line.split()[:2]), line.split()) for line in f.readlines()]
        self.buffer = OrderedDict(lines)

    def save_buffer(self):
        with open(self.buffer_file_path, 'w') as f:
            for key, value in self.buffer.items():
                f.write(' '.join(value) + '\n')

    def push_command(self, command):
        key = command[:2]
        value = command
        self.buffer[key] = value
        self.save_buffer()

    def pop(self):
        key, value = self.buffer.popitem()
        self.save_buffer()
        return value

    def is_able_to_fast_read(self, cmd):
        keys = list(self.buffer.keys())[::-1]
        for command in keys:
            if command[0] == 'W' and command[1] == cmd[1]:
                return True
            elif command[0] == 'E' and command[1] <= cmd[1] <= command[1] + command[2]:
                return True
        return False

    def get_read_fast(self, cmd):
        keys = list(self.buffer.keys())[::-1]
        for command in keys:
            if command[0] == 'W' and command[1] == cmd[1]:
                return self.buffer[command][2]
            elif command[0] == 'E' and command[1] <= cmd[1] <= command[1]+command[2]:
                return 0x00000000

    def flush(self):
        cmd_list = [value for key, value in self.buffer.items()]
        self.buffer.clear()
        self.save_buffer()
        return cmd_list[::-1]

    def optimize(self):

        pass

    def need_flush(self):
        return len(self.buffer) >= 10

