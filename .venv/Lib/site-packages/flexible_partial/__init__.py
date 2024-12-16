import inspect
from copy import deepcopy


def copy_func(f):
    if callable(f):
        if inspect.ismethod(f) or inspect.isfunction(f):
            g = lambda *args, **kwargs: f(*args, **kwargs)
            t = list(filter(lambda prop: not ("__" in prop), dir(f)))
            i = 0
            while i < len(t):
                setattr(g, t[i], getattr(f, t[i]))
                i += 1
            return g
    dcoi = deepcopy([f])
    return dcoi[0]


class FlexiblePartial:
    def __init__(self, func, this_args_first=True, *args, **kwargs):

        self.this_args_first = this_args_first
        try:
            self.modulename = func.__module__
        except Exception:
            self.modulename = ""

        try:
            self.functionname = func.__name__
        except Exception:
            try:
                self.functionname = func.__qualname__
            except Exception:
                self.functionname = "func"

        try:
            self.f = copy_func(func)
        except Exception:
            self.f = func
        try:
            self.args = copy_func(list(args))
        except Exception:
            self.args = args

        try:
            self.kwargs = copy_func(kwargs)
        except Exception:
            try:
                self.kwargs = kwargs.copy()
            except Exception:
                self.kwargs = kwargs

        self.name_to_print = self._create_name()

    def _create_name(self):
        if self.modulename != "":
            stra = self.modulename + "." + self.functionname + "("
        else:
            stra = self.functionname + "("

        for _ in self.args:
            stra = stra + repr(_) + ", "
        for key, item in self.kwargs.items():
            stra = stra + str(key) + "=" + repr(item) + ", "
        stra = stra.rstrip().rstrip(",")
        stra += ")"
        if len(stra) > 100:
            stra = stra[:95] + "...)"
        return stra

    def __call__(self, *args, **kwargs):
        newdic = {}
        newdic.update(self.kwargs)
        newdic.update(kwargs)
        if self.this_args_first:
            return self.f(*self.args, *args, **newdic)

        else:

            return self.f(*args, *self.args, **newdic)

    def __str__(self):
        return self.name_to_print

    def __repr__(self):
        return self.__str__()


class FlexiblePartialOwnName:
    r"""
    FlexiblePartial(
            remove_file,
            "()",
            True,
            fullpath_on_device=x.aa_fullpath,
            adb_path=adb_path,
            serialnumber=device,
        )

    """

    def __init__(
        self, func, funcname: str, this_args_first: bool = True, *args, **kwargs
    ):

        self.this_args_first = this_args_first
        self.funcname = funcname
        try:
            self.f = copy_func(func)
        except Exception:
            self.f = func
        try:
            self.args = copy_func(list(args))
        except Exception:
            self.args = args

        try:
            self.kwargs = copy_func(kwargs)
        except Exception:
            try:
                self.kwargs = kwargs.copy()
            except Exception:
                self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        newdic = {}
        newdic.update(self.kwargs)
        newdic.update(kwargs)
        if self.this_args_first:
            return self.f(*self.args, *args, **newdic)

        else:

            return self.f(*args, *self.args, **newdic)

    def __str__(self):
        return self.funcname

    def __repr__(self):
        return self.funcname
