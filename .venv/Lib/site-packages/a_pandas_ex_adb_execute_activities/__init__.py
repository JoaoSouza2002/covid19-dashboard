import subprocess
from typing import Any
import inspect
from copy import deepcopy

import pandas as pd
import regex
from flatten_everything import flatten_everything, ProtectedTuple
from subprocess_print_and_capture import (
    execute_subprocess_multiple_commands_with_timeout_bin,
)

findactregex = regex.compile(
    r"[\n\r]+\s{8}([a-f0-9]{7})\s+([^\n\r]+)(.*?)(?=[\r\n][^\n\r]*?[\r\n]\s{8}\w)",
    flags=regex.DOTALL | regex.MULTILINE,
)
actsplitregex = regex.compile(r"[=:]\s*")
act2splitregex = regex.compile(r",[\s]+")
wordstartregex = regex.compile(r"^\w")
tenspaceregex = regex.compile(r"^\s{10}")


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


def execute_activity_via_adb_shell(
    adb_path,
    deviceserial,
    cmd,
    add_to_command="",
    stop=False,
    wait=False,
    exit_keys="ctrl+x",
    timeout=None,
):
    if wait:
        cmd = regex.sub(r"^.*?\bam start\b", r" \g<0> -W", cmd)
    if stop:
        cmd = regex.sub(r"^.*?\bam start\b", r" \g<0> -S", cmd)
    cmd = cmd + f" {add_to_command}"
    print(f"Executing: {cmd}")
    execute_multicommands_adb_shell(
        adb_path=adb_path,
        device_serial=deviceserial,
        subcommands=[cmd],
        exit_keys=exit_keys,
        print_output=True,
        timeout=timeout,
    )


def adb_shell(
    adb_path, deviceserial, cmd, funcname,
):
    return FlexiblePartial(
        execute_activity_via_adb_shell, funcname, True, adb_path, deviceserial, cmd,
    )


class FlexiblePartial:
    def __init__(
        self, func: Any, funcname: str, this_args_first: bool = True, *args, **kwargs
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


def execute_multicommands_adb_shell(
    adb_path,
    device_serial,
    subcommands: list,
    exit_keys: str = "ctrl+x",
    print_output=True,
    timeout=None,
):
    if not isinstance(subcommands, list):
        subcommands = [subcommands]

    return execute_subprocess_multiple_commands_with_timeout_bin(
        cmd=f"{adb_path} -s {device_serial} shell",
        subcommands=subcommands,
        exit_keys=exit_keys,
        end_of_printline="",
        print_output=print_output,
        timeout=timeout,
    )


def execute_command_adb(adb_path, device_serial, command: str):
    proc = subprocess.run(
        f"{adb_path} -s {device_serial} {command}", capture_output=True
    )
    return (
        proc.stdout.decode("utf-8", "ignore"),
        proc.stderr.decode("utf-8", "ignore"),
        proc.returncode,
    )


def connect_to_adb(adb_path, deviceserial):
    _ = subprocess.run(f"{adb_path} start-server", capture_output=True, shell=False)
    _ = subprocess.run(
        f"{adb_path} connect {deviceserial}", capture_output=True, shell=False
    )


def get_all_activities_from_package(adb_path, device_serial, df):
    df2 = df.copy()
    funcol = [
        x
        for x in df.columns.to_list()
        if x
        not in ["hexno", "filt", "Action", "Category", "name_of_function", "command",]
    ]
    for key, item in df.iterrows():
        n = item.package
        funktionsname_n = ""
        if len(n) == 0:
            continue
        else:
            n = f'-n "{n}"'
            funktionsname2 = str(item.package)

            funktionsname_n = regex.sub(r"\W+", "_", funktionsname2).strip("_")
        try:
            a = item.Action
        except Exception:
            a = ""
        funktionsname_a = ""
        if len(a) == 0:
            a = ""
        else:
            a = f'-a "{a}"'
            funktionsname_a = regex.sub(fr"^(.*?)\.([A-Z_]+)$", r"\g<2>", item.Action)
        try:
            c = item.Category
        except Exception:
            c = ""
        funktionsname_c = ""

        if len(c) == 0:
            c = ""
        else:
            c = f'-c "{c}"'
            funktionsname_c = regex.sub(fr"^(.*?)\.([A-Z_]+)$", r"\g<2>", item.Category)
        t = ""
        funktionsname_t = ""
        if "Type" in df.columns:
            if len(item["Type"]) > 0:
                t = f"-t \"{item['Type']}\""
                funktionsname_t = regex.sub(r"\W+", "_", item["Type"]).strip("_")

        s = ""
        funktionsname_s = ""
        if "Scheme" in df.columns:
            if len(item["Scheme"]) > 0:
                s = f"{item['Scheme']}".strip()

                funktionsname_s = regex.sub(r"\W+", "_", item["Scheme"].strip()).strip(
                    "_"
                )

        command = f"am start {a} {c} {n} {t}".strip()
        command_function_description = f"{a}\n{c}\n{n}\n{t}".strip()
        command_function_description = "\n".join(
            [
                y.strip()
                for y in regex.split(r"\s*[\n\r]+\s*+", command_function_description)
                if y.strip() != ""
            ]
        ).strip()

        finalname = regex.sub(
            r"\W+",
            "_",
            f"{funktionsname_n}__{funktionsname_a}__{funktionsname_c}__{funktionsname_t}__{funktionsname_s}",
        ).strip("_")
        df2.at[key, "name_of_function"] = finalname
        df2.at[key, "command"] = command

        infos = "\n".join([f"{y}: {item[y]}" for y in funcol])
        functiondescription = f"{command_function_description}\n" + infos.strip()
        df2.at[key, "function_description"] = functiondescription

    df = df2.copy()
    indextochange = df.loc[~df.Action.str.contains(r"\.[A-Z_]+$")].index.copy()
    df.loc[indextochange, "command"] = df.loc[indextochange].command.str.replace(
        r'^(am start\s+-a\s+"[^"]+").*', r"\g<1>", regex=True
    )
    df.loc[indextochange, "function_description"] = df.loc[indextochange, "command"]
    df["call"] = df.apply(
        lambda aq: adb_shell(
            adb_path=adb_path,
            deviceserial=device_serial,
            cmd=aq["command"],
            funcname=aq["function_description"],
        ),
        axis=1,
    )
    df = (
        df.drop_duplicates(subset="name_of_function")
        .set_index("name_of_function")
        .T.drop(["filt", "hexno", "function_description"])
    )

    return df


def _get_activity_dataframe(
    adb_path,
    deviceserial,
    package,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"""dumpsys package {package}"""],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    baba = "".join([x.decode("utf-8", "ignore") for x in xx])
    df = pd.DataFrame.from_records(
        [
            [y.strip().splitlines() for y in flatten_everything(x)]
            for x in findactregex.findall(baba)
        ]
    )
    df[0] = df[0].apply(lambda x: x[0])
    pack = df[1].apply(lambda x: x[0]).str.split(n=2, expand=True)
    df5 = df[2].apply(
        lambda __: [
            j
            for j in flatten_everything(
                [
                    ProtectedTuple(
                        tuple(
                            [
                                q.strip()
                                for q in actsplitregex.split(p)
                                if q.strip() != ""
                            ]
                        )
                    )
                    for p in (
                        flatten_everything(
                            [
                                act2splitregex.split(k)
                                for k in __
                                if wordstartregex.search(k) is not None
                                or tenspaceregex.search(k) is not None
                            ]
                        )
                    )
                ]
            )
            if len(j) == 2
        ]
    )
    df5 = pd.concat(
        df5.apply(
            lambda v: pd.DataFrame.from_records(
                [(f[0].strip(' "'), f[1].strip(' "')) for f in v]
            )
            .groupby(0, as_index=False)
            .agg(
                {
                    1: lambda x: x,
                    0: lambda x: [f"{y}_{ini}" for ini, y in enumerate(x)],
                }
            )
            .assign(**{"indi": lambda i: i[0].apply(lambda n: n[0])})
            .set_index("indi")
            .drop(columns=0)
            .T
        ).to_list()
    ).reset_index(drop=True)
    df = pd.concat([pack, df5], ignore_index=True, axis=1)
    df6 = df.copy()
    for col in df.columns:
        df6 = df6.explode(col)
    df = df6.reset_index(drop=True).copy()
    df.columns = ["package", "filt", "hexno"] + [x[:-2] for x in df5.columns.to_list()]
    df = df.fillna("").drop_duplicates().reset_index(drop=True)
    return df


def get_activities_df_from_package(
    adb_path: str, deviceserial: str, packagename: str
) -> pd.DataFrame:
    connect_to_adb(adb_path, deviceserial)
    df = _get_activity_dataframe(
        adb_path,
        deviceserial,
        package=packagename,
        exit_keys="ctrl+x",
        print_output=False,
        timeout=None,
    )
    df = get_all_activities_from_package(adb_path, deviceserial, df)
    return df


def get_all_activities(adb_path: str, deviceserial: str) -> pd.DataFrame:
    connect_to_adb(adb_path, deviceserial)

    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[f"""pm -l"""],
        exit_keys="ctrl+x",
        print_output=True,
        timeout=None,
    )
    allp = [x.decode("utf-8", "ignore").strip().split(":")[-1] for x in xx]

    allac = []
    for p in allp:
        try:
            dfa = get_activities_df_from_package(adb_path, deviceserial, p).T
            if not dfa.empty:
                dfa["packagename"] = p
                dfa = dfa.reset_index()
                allac.append(dfa.copy())
        except Exception as fe:
            # print(fe, p)
            continue
    df2 = pd.concat(allac, ignore_index=True)
    df2 = df2.fillna("")
    return df2


def pd_add_adb_execute_activities():
    pd.Q_ADB_all_activities_to_df = get_all_activities
    pd.Q_ADB_activities_from_package_to_df = get_activities_df_from_package


