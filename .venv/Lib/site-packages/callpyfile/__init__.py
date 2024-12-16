import os
import sys
import dill
import subprocess
import io
from functools import wraps


def to_stdout(f_py=None, kill_if_exception=True):
    def globals_from_dict(di, name):
        for key, item in di.items():
            setattr(sys.modules[name], key, item)

    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            stdout = sys.stdout
            sys.stdout = io.StringIO()
            image_data = sys.stdin.buffer.read()
            f = dill.loads(image_data)
            globals_from_dict(f, "__main__")
            allb = func(*args, **kwargs)
            output_data = io.BytesIO()
            output_data.write(
                b"STARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTART"
                + dill.dumps(allb)
                + b"ENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDEND"
            )
            sys.stdout = stdout
            sys.stdout.flush()
            sys.stdout.buffer.write(output_data.getvalue())
            return None

        return wrapper

    try:
        return _decorator(f_py) if callable(f_py) else _decorator
    except Exception as fe:
        if kill_if_exception:
            os._exit()


def run_py_file(
    variables,
    pyfile,
    activate_env_command="",
    pythonexe=sys.executable,
    raise_exception=False,
):

    pyfile = os.path.normpath(pyfile)
    pythonexe = os.path.normpath(pythonexe)
    executecommand = [pythonexe, pyfile]
    if activate_env_command:
        if isinstance(activate_env_command, tuple):
            activate_env_command = list(activate_env_command)
        executecommand = activate_env_command + ["&"] + executecommand
    ii = dill.dumps(variables)
    p = None
    try:
        DEVNULL = open(os.devnull, "wb")
        p = subprocess.run(
            executecommand, input=ii, stdout=subprocess.PIPE, stderr=DEVNULL
        )
    finally:
        try:
            DEVNULL.close()
        except Exception as fe:
            print(fe)

    try:
        output_data = p.stdout
        output_data = output_data.split(
            b"STARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTART"
        )[-1]
        output_data = output_data.split(
            b"ENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDEND"
        )[0]
        return dill.loads(output_data)
    except Exception as fa:
        if raise_exception:
            raise fa
        print(fa)
        return None
