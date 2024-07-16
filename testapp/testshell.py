import re

from testapp import command

EXECUTE_VALID_WO_ARGS = 2

EXECUTE_VALID_WITH_ARGS = 1

EXECUTE_INVALID = 0


def is_between_0_and_99(s):
    try:
        num = int(s)
        return 0 <= num <= 99
    except ValueError:
        return False


def is_valid_hex(s):
    # 정규식으로 형식을 먼저 확인
    if re.fullmatch(r'0x[0-9A-Fa-f]{8}', s):
        try:
            # 16진수로 변환하여 범위를 확인
            num = int(s, 16)
            return 0x00000000 <= num <= 0xFFFFFFFF
        except ValueError:
            return False
    return False


class TestShell:
    cmd_if_dict = {
        "write": command.Write,
        "read": command.Read,
        "exit": command.Exit,
        "help": command.Help,
        "fullwrite": command.FullWrite,
        "fullread": command.FullRead,
        # "testapp1": command.Testapp1,
        # "testapp2": command.Testapp2,
    }

    def execute(self, cmd: str):
        if not self.is_valid_cmd(cmd):
            print(cmd)
            return EXECUTE_INVALID

        cmd_option, cmd_args = self.parse_args(cmd)

        cmd_if = self.cmd_if_dict[cmd_option]()
        if cmd_args is not None:
            print(cmd_option, cmd_args)
            cmd_if.run(cmd_args)
            return EXECUTE_VALID_WITH_ARGS

        print(cmd_option, cmd_args)
        cmd_if.run()
        return EXECUTE_VALID_WO_ARGS

    def is_valid_cmd(self, cmd: str) -> bool:
        if self.valid_cmd(cmd):
            return True
        else:
            return False

    def valid_cmd(self, cmd):
        """
        유효성 검사 수행
        """
        cmd_option_to_args_dict = {
            "write": 2,
            "read": 1,
            "help": 0,
            "fullwrite": 1,
            "fullread": 0,
            "testapp1": 0,
            "testapp2": 0
        }
        cmd_list = cmd.split(" ")
        cmd_option = cmd_list[0]
        n_args = len(cmd_list) - 1
        if cmd_option not in cmd_option_to_args_dict.keys():
            print("Command does not exist")
            return False
        if cmd_option_to_args_dict[cmd_option] != n_args:
            print("The number of argument does not match")
            return False
        # 0. exit (구현 필요 x), help, fullread , testapp1, testapp2
        if n_args == 0:
            return True
        # 1. write
        if cmd_option == "write":
            n_lba = cmd_list[1]
            value = cmd_list[2]
            if not is_between_0_and_99(n_lba):
                return False
            if not is_valid_hex(value):
                return False
            return True
        # 2. read
        if cmd_option == "read":
            n_lba = cmd_list[1]
            if is_between_0_and_99(n_lba):
                return True
            else:
                return False

        # 3. fullwrite
        if cmd_option == "fullwrite":
            value = cmd_list[1]
            if is_valid_hex(value):
                return True
            else:
                return False
        return True

    def parse_args(self, cmd: str):
        cmd_list = cmd.split(" ")
        cmd_option = cmd_list[0]
        if len(cmd_list) > 1:
            cmd_args = cmd_list[1:]
            return cmd_option, cmd_args
        return cmd_option, None


def main():
    testshell = TestShell()
    while True:
        cmd = input("> ")
        if cmd == "exit":
            break
        testshell.execute(cmd)
    return


if __name__ == "__main__":
    main()
