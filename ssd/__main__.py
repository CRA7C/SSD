import os
import sys
from typing import Union

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ssd.solidstatedrive import SolidStateDrive
from ssd.common import LBA_LOWER_LIMIT, LBA_UPPER_LIMIT, is_valid_hex
from ssd.command_buffer import CommandBuffer
from ssd.command import CommandFactory, Command, ReadCommand, WriteCommand, EraseCommand


class SSDRunner:
    """
    SSDRunner 클래스는 가상 SSD의 명령을 처리하고 실행하는 역할을 합니다.

    Attributes:
        ssd (SolidStateDrive): 가상 SSD 객체
        option_buf (CommandBuffer): 명령 버퍼 객체
    """
    option_buf: CommandBuffer

    def __init__(self):
        self.ssd = SolidStateDrive()
        self.option_buf = CommandBuffer()

    @staticmethod
    def is_valid_command() -> bool:
        """
        명령어의 유효성을 검사합니다.

        Raises:
            ValueError: 유효하지 않은 명령어인 경우 예외를 발생시킵니다.

        Returns:
            bool: 명령어가 유효한 경우 True를 반환합니다.
        """
        if sys.argv[1] == 'F':
            return True

        if len(sys.argv) < 3:
            raise ValueError("명령을 수행하기 위한 인자가 부족합니다. ex) ssd R 20/ssd W 20 0x1289CDEF/ssd E 10 3")

        if sys.argv[1] not in ('R', 'W', 'E', 'F'):
            raise ValueError('R, W, E, F 중 하나를 사용해주세요.(대문자)')

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
        """
        명령 버퍼를 비우고 명령어를 실행합니다.
        """
        cmd_list = self.option_buf.flush()
        for cmd in cmd_list:
            self.execute_command(cmd)

    def run(self):
        """
        주어진 명령어를 파싱하고 실행합니다.
        """
        cmd: Command = CommandFactory().parse_command(sys.argv[1:])
        if cmd.option == 'F':
            self.buff_flush()
        elif cmd.option == 'R':
            if self.option_buf.is_able_to_fast_read(cmd):
                self.ssd.read_fast(self.option_buf.get_read_fast(cmd))
            else:
                self.execute_command(cmd)
        elif cmd.option in ('W', 'E'):
            if self.option_buf.need_flush():
                self.buff_flush()
            self.option_buf.push_command(cmd)

    def execute_command(self, command: Union[ReadCommand, WriteCommand, EraseCommand]):
        """
        특정 명령어를 실행합니다.

        Args:
            command: 실행할 명령어 객체
        """
        cmd_opt = command.option
        if cmd_opt == 'R':
            self.ssd.read(command.lba)
        elif cmd_opt == 'W':
            self.ssd.write(command.lba, command.value)
        elif cmd_opt == 'E':
            self.ssd.erase(command.lba, command.size)


if __name__ == '__main__':
    runner = SSDRunner()
    if runner.is_valid_command():
        runner.run()
