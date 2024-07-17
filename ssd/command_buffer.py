from pathlib import Path
from collections import OrderedDict

BUFFER_FILE_PATH = Path(__file__).parent / 'buffer.txt'


class Command:
    def __init__(self, cmd, args):
        self.cmd = cmd
        self.args = args

    def get_value(self):
        return self.cmd, *self.args
    @staticmethod
    def get_command(buffer_data):
        cmd = buffer_data[0]
        args = [int(value) for value in buffer_data[1:]]
        return Command(cmd, args)

    @staticmethod
    def create_command(cmd_str):
        cmd = cmd_str[0]
        if cmd == 'W':
            args = (int(cmd_str[1]), int(cmd_str[2],16))
        elif cmd == 'R':
            args = (int(cmd_str[1]),)
        elif cmd == 'E':
            args = (int(cmd_str[1]), int(cmd_str[2]))
        else:
            args = tuple(cmd_str[1:])

        return Command(cmd, args)


class CommandBuffer:
    def __init__(self):
        self.buffer_file_path: Path = Path(BUFFER_FILE_PATH)
        self.buffer = []
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
            self.buffer = [Command.get_command(line.split()) for line in f.readlines()]

    def save_buffer(self):
        with open(self.buffer_file_path, 'w') as f:
            for data in self.buffer:
                f.write(' '.join([str(d) for d in data.get_value()]) + '\n')

    def push_command(self, command):
        self.buffer.append(command)
        self.save_buffer()

    def pop(self):
        value = self.buffer.pop()
        self.save_buffer()
        return value

    def is_able_to_fast_read(self, cmd):
        for command in self.buffer[::-1]:
            if command.cmd == 'W' and command.args[0] == cmd.args[0]:
                return True
            elif command.cmd == 'E' and command.args[0] <= cmd.args[0] < command.args[0] + command.args[1]:
                return True
        return False

    def get_read_fast(self, cmd):
        for command in self.buffer[::-1]:
            if command.cmd == 'W' and command.args[0] == cmd.args[0]:
                return command.args[1]
            elif command.cmd == 'E' and command.args[0] <= cmd.args[0] < command.args[0] + command.args[1]:
                return 0x00000000

    def flush(self):
        cmd_list = [value for value in self.buffer]
        self.buffer.clear()
        self.save_buffer()
        return cmd_list[::-1]

    def optimize(self):
        pass

    def need_flush(self):
        return len(self.buffer) > 10
