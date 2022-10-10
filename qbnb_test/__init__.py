import sys
from os import path


def set_up_path():
    """Function we use so that modules are being imported correctly on
        vs code
    """
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


path_setup = set_up_path()
