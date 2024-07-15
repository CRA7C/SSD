from testapp import command


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
        cmd = self.convert_to_valid_cmd(cmd)
        if cmd == "INVALID COMMAND":
            print(cmd)
            return

        cmd_option, cmd_args = self.parse_args(cmd)

        cmd_if = self.cmd_if_dict[cmd_option]()
        if cmd_args is not None:
            print(cmd_option, cmd_args)
            cmd_if.run(cmd_args)
        else:
            print(cmd_option, cmd_args)
            cmd_if.run()

    def convert_to_valid_cmd(self, cmd: str) -> str:
        if self.valid_cmd(cmd):
            return cmd
        else:
            return "INVALID COMMAND"

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
