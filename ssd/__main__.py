import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ssd.solidstatedrive import SolidStateDrive
from ssd.common import LBA_LOWER_LIMIT, LBA_UPPER_LIMIT, is_valid_hex
from ssd.command_buffer import CommandBuffer, Command


class SSDRunner:
    def __init__(self):
        self.ssd = SolidStateDrive()
        self.cmd_buf = CommandBuffer()

    @staticmethod
    def is_valid_command():
        if len(sys.argv) < 3:
            raise ValueError("명령을 수행하기 위한 인자가 부족합니다. ex) ssd R 20/ssd W 20 0x1289CDEF/ssd E 10 3")

        if sys.argv[1] not in ('R', 'W', 'E'):
            raise ValueError('R, W, E 중 하나를 사용해주세요.(대문자)')

        if not sys.argv[2].isdigit():
            raise ValueError('LBA는 숫자여야합니다.')

        if not LBA_LOWER_LIMIT <= int(sys.argv[2]) <= LBA_UPPER_LIMIT:
            raise ValueError(f'LBA는 {LBA_LOWER_LIMIT} ~ {LBA_UPPER_LIMIT} 여야합니다.')

        if sys.argv[1] == 'W':
            if len(sys.argv) < 4:
                raise ValueError('W 명령에는 value가 필요합니다.')
            if not is_valid_hex(sys.argv[3]):
                raise ValueError('value는 0x00000000 형식이여야 합니다.')
        if sys.argv[1] == 'E':
            if len(sys.argv) < 4:
                raise ValueError('E 명령에는 시작 LBA, 지울 데이터 갯수가 필요합니다.')
            if not sys.argv[3].isdigit():
                raise ValueError('지울 데이터 갯수는 숫자여야합니다.')
            if not 1 <= int(sys.argv[3]) <= 10:
                raise ValueError('지울 데이터 갯수는 1이상 10이하만 가능합니다.')
        return True

    def buff_flush(self):
        cmd_list = self.cmd_buf.flush()
        for cmd in cmd_list:
            self.execute_command(cmd)

    def run(self):
        cmd = Command.create_command(sys.argv[1:])
        if cmd.cmd == 'F':
            self.buff_flush()
        elif cmd.cmd == 'R':
            if self.cmd_buf.is_able_to_fast_read(cmd):
                value = self.cmd_buf.get_read_fast(cmd)
                self.ssd.read_fast(value)
            else:
                self.execute_command(cmd)
        elif cmd.cmd in ('W', 'E'):
            self.cmd_buf.push_command(cmd)
            if self.cmd_buf.need_flush():
                self.buff_flush()

    def execute_command(self, command):
        cmd = command.cmd
        if cmd == 'R':
            self.ssd.read(command.args[0])
        elif cmd == 'W':
            self.ssd.write(command.args[0], command.args[1])
        elif cmd == 'E':
            self.ssd.erase(command.args[0], command.args[1])


if __name__ == '__main__':
    runner = SSDRunner()
    if runner.is_valid_command():
        runner.run()
