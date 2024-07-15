from testapp import command

EXECUTE_VALID_WO_ARGS = 2

EXECUTE_VALID_WITH_ARGS = 1

EXECUTE_INVALID = 0


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
    cmd = input("> ")
    testshell.execute(cmd)
    return


if __name__ == "__main__":
    main()
