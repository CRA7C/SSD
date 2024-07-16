from .write import Write
from .read import Read
from .exit import Exit
from .help import Help
from .fullwrite import FullWrite
from .fullread import FullRead

COMMAND_DICT = {
    "write": Write,
    "read": Read,
    "exit": Exit,
    "help": Help,
    "fullwrite": FullWrite,
    "fullread": FullRead,
    # "testapp1": command.Testapp1,
    # "testapp2": command.Testapp2,
}
__all__ = ['Write', 'Read', 'Exit', 'Help', 'FullWrite', 'FullRead',
           'COMMAND_DICT']
