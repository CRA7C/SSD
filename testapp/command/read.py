from testapp.command.__interface import CommandInterface
from tests.util import get_ssd_result


class Read(CommandInterface):
    def run(self, *args, **kwarg):
        self.valid_check(args)

        read_cmd = f'ssd.py R {args[0]}'
        run_subprocess(read_cmd)

        return get_ssd_result()

    def valid_check(self, args):
        if len(args) != 1:
            raise ValueError
        if args[0] < 0:
            raise ValueError
        elif args[0] >= 100:
            raise ValueError


