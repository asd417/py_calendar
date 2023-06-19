import os
import sys

def get_script_path():
    if getattr(sys, 'frozen', False):
        # When running as an executable
        return os.path.dirname(sys.executable)
    else:
        # When running as a script
        main_script = sys.modules['__main__']
        if hasattr(main_script, '__file__'):
            return os.path.dirname(os.path.realpath(main_script.__file__))
        else:
            return os.getcwd()
