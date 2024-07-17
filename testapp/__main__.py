import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from testapp.testshell import main  # noqa
from testapp.scripts import run_test_script_file

if __name__ == "__main__":
    if len(sys.argv) == 2:
        run_test_script_file(sys.argv[1])
    else:
        main()
