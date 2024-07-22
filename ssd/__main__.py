"""
`python -m ssd` 동작 시 실행되는 파일입니다.
"""
import os
import sys
from typing import Union

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ssd.solidstatedrive import SolidStateDrive
from ssd.command_buffer import CommandBuffer
from ssd.command import CommandFactory, Command, ReadCommand, WriteCommand, EraseCommand
from my_logger import Logger


class SSDRunner:
    """
    SSDRunner 클래스는 가상 SSD의 명령을 처리하고 실행하는 역할을 합니다.

    Attributes:
        ssd (SolidStateDrive): 가상 SSD 객체
        option_buf (CommandBuffer): 명령 버퍼 객체
    """

    def __init__(self):
        Logger().debug("[SSD] Start SSDRunner")
        self.ssd = SolidStateDrive()
        self.option_buf = CommandBuffer()

    def __del__(self):
        Logger().debug("[SSD] Finish SSDRunner")

    def buff_flush(self):
        """
        명령 버퍼를 비우고 명령어를 실행합니다.
        """
        Logger().debug("Buffer Flash")
        cmd_list = self.option_buf.flush()
        for cmd in cmd_list:
            self.execute_command(cmd)

    def run(self, cmd: Command):
        """
        주어진 명령어를 파싱하고 실행합니다.
        """
        Logger().debug(f"[SSD] Received CMD : {cmd.get_value()}")

        if cmd.option == 'F':
            self.buff_flush()
        elif cmd.option == 'R':
            if self.option_buf.is_able_to_fast_read(cmd):
                read_value = self.option_buf.get_read_fast(cmd)
                self.ssd.read_fast(read_value)
                Logger().debug(f"Read Fast : {read_value}")
            else:
                self.execute_command(cmd)
                Logger().debug("Read from NAND")
        elif cmd.option in ('W', 'E'):
            if self.option_buf.need_flush():
                self.buff_flush()
            self.option_buf.push_command(cmd)
            Logger().debug("Push into buffer")

    def execute_command(self, command: Union[ReadCommand, WriteCommand, EraseCommand]):
        """
        특정 명령어를 실행합니다.

        Args:
            command: 실행할 명령어 객체
        """
        Logger().debug(f"Execute CMD : {command.get_value()}")
        cmd_opt = command.option
        if cmd_opt == 'R':
            self.ssd.read(command.lba)
        elif cmd_opt == 'W':
            self.ssd.write(command.lba, command.value)
        elif cmd_opt == 'E':
            self.ssd.erase(command.lba, command.size)


if __name__ == '__main__':
    cmd_ = CommandFactory.parse_command(sys.argv[1:])
    SSDRunner().run(cmd_)
