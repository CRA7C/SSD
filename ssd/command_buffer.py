from pathlib import Path
from ssd.command import Command, CommandFactory

BUFFER_FILE_PATH = Path(__file__).parent / 'buffer.txt'


class CommandBuffer:
    def __init__(self):
        self.buffer_file_path: Path = Path(BUFFER_FILE_PATH)
        self.buffer = []
        self.initialize()

    def initialize(self):
        # 만일 buffer.txt 파일이 없으면, 초기화 된 파일 생성
        if not self.buffer_file_path.exists():
            with open(self.buffer_file_path, 'w', encoding='utf-8'):
                pass
        else:
            self.load_buffer()

    def load_buffer(self):
        with open(self.buffer_file_path, 'r') as f:
            self.buffer = [CommandFactory().parse_command(line.split()) for line in f.readlines()]

    def save_buffer(self):
        with open(self.buffer_file_path, 'w') as f:
            f.write(self.get_saved_data())

    def get_saved_data(self):
        txt = []
        for data in self.buffer:
            txt.append(' '.join(data.get_value()) + '\n')
        return ''.join(txt)

    def push_command(self, command):
        self.buffer.append(command)
        self.optimize()
        self.save_buffer()

    def pop(self):
        value = self.buffer.pop()
        self.save_buffer()
        return value

    def is_able_to_fast_read(self, cmd):
        for command in self.buffer[::-1]:
            if command.option == 'W' and command.lba == cmd.lba:
                return True
            elif command.option == 'E' and command.lba <= cmd.lba < command.lba + command.size:
                return True
        return False

    def get_read_fast(self, cmd):
        for command in self.buffer[::-1]:
            if command.option == 'W' and command.lba == cmd.lba:
                return command.value
            elif command.option == 'E' and command.lba <= cmd.lba < command.lba + command.size:
                return 0x00000000

    def flush(self):
        cmd_list = [value for value in self.buffer]
        self.buffer.clear()
        self.save_buffer()
        return cmd_list

    def optimize(self):
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
    def merge_write_with_erase(erase_commands, key):
        for erase in erase_commands:
            if erase[1] <= key[1] and key[2] <= erase[2]:
                return True
        return False

    def need_flush(self):
        return len(self.buffer) > 10
