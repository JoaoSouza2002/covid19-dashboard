import inspect
import os
import subprocess
from copy import deepcopy
from typing import Any

import pandas as pd
import regex
from subprocess_print_and_capture import (
    execute_subprocess_multiple_commands_with_timeout_bin,
)
pulledfilecompiled = regex.compile(r"1\s+file\s+pulled", flags=regex.IGNORECASE)


def pull_with_cat(
    save_in_folder,
    folder_on_device,
    fullpath_on_device,
    adb_path,
    device_serial,
    exit_keys: str = "ctrl+x",
    print_output=False,
    timeout=None,
):
    # df.loc[(~df.aa_fullpath.str.contains('mnt/|system/|boot/|dev/|sdcard/|storage/|sys/|acct/')) & (df.aa_symlink.isna()) & (df.aa_size > 0) & (~df.aa_rights.str.contains('^d'))].ff_pull_file_cat.apply(lambda x:x('f:\\gvbadsasww', timeout=15))
    # print(save_in_folder, folder_on_device, fullpath_on_device, adb_path)
    try:
        savepath_folder = (
            os.path.join(save_in_folder, folder_on_device)
            .replace("/", os.sep)
            .replace("\\", os.sep)
        )

        savepath = os.path.normpath(os.path.join(save_in_folder, fullpath_on_device))
        if not os.path.exists(savepath_folder):
            os.makedirs(savepath_folder)
        command = f"""su -- cat {fullpath_on_device}"""
        if not isroot(adb_path, device_serial):
            command = f"""cat {fullpath_on_device}"""

        filax = b"".join(
            [
                x.replace(b"\r\n", b"\n")
                for x in execute_multicommands_adb_shell(
                    adb_path,
                    device_serial,
                    [command],
                    exit_keys=exit_keys,
                    print_output=print_output,
                    timeout=timeout,
                )
            ]
        )
        try:
            with open(savepath, mode="wb") as f:
                f.write(filax)
        except Exception:
            pass
        return savepath
    except Exception as fe:
        print(fe, end='\r')
    return pd.NA

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


def connect_to_adb(adb_path, deviceserial):
    _ = subprocess.run(f"{adb_path} start-server", capture_output=True, shell=False)
    _ = subprocess.run(
        f"{adb_path} connect {deviceserial}", capture_output=True, shell=False
    )


def remove_file(
    fullpath_on_device, adb_path, serialnumber, exit_keys="ctrl+x", timeout=None
):
    excutecommand = f'''rm -f "{fullpath_on_device}"'''
    if isroot(adb_path, deviceserial=serialnumber):
        excutecommand = f'''su -- rm -f "{fullpath_on_device}"'''

    print(
        f"{excutecommand} - Deleting {fullpath_on_device}                         ",
        end="\n",
    )

    return "".join(
        [
            o.decode("utf-8", "replace")
            for o in execute_multicommands_adb_shell(
                adb_path,
                device_serial=serialnumber,
                subcommands=[excutecommand],
                exit_keys=exit_keys,
                print_output=True,
                timeout=timeout,
            )
        ]
    )


def pull_adb_file(
    save_in_folder,
    folder_on_device,
    fullpath_on_device,
    adb_path,
    serialnumber,
    exit_keys="ctrl+x",
    timeout=None,
):
    print(save_in_folder, folder_on_device, fullpath_on_device, adb_path)
    savepath_folder = (
        os.path.join(save_in_folder, folder_on_device)
        .replace("/", os.sep)
        .replace("\\", os.sep)
    )

    savepath = os.path.normpath(os.path.join(save_in_folder, fullpath_on_device))
    if not os.path.exists(savepath_folder):
        os.makedirs(savepath_folder)

    ps = execute_subprocess_multiple_commands_with_timeout_bin(
        f'"{adb_path}" -s {serialnumber} pull "{fullpath_on_device}" "{savepath}"',
        subcommands=[],
        exit_keys=exit_keys,
        end_of_printline="",
        print_output=True,
        timeout=timeout,
    )

    output = "".join([x.decode("utf-8", "replace") for x in ps])
    # print(output)
    if pulledfilecompiled.search(output) is not None:
        return True
    else:
        return False


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


def isroot(
    adb_path, deviceserial, exit_keys="ctrl+x", print_output=False, timeout=None
):
    # from https://wuseman.se/
    roa = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            f"""which su -- &> /dev/null
    if [[ $? = "0" ]]; then
        echo "True"
    else
        echo "False"
    fi"""
        ],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    isrooted = False
    if roa[0].decode("utf-8", "ignore").strip() == "True":
        isrooted = True

    return isrooted


def get_folder_df(device: str, adb_path: str,folder='') -> pd.DataFrame:
    connect_to_adb(adb_path=adb_path, deviceserial=device)
    executecommand = f'''cd {folder} && ls -R -i -H -las -s "////////////$PWD/"*'''
    if isroot(adb_path, device, print_output=True):
        executecommand = f'su -c \'cd {folder} && ls -R -i -H -las -s "////////////$PWD/"\'*'
    data = execute_multicommands_adb_shell(
        adb_path, device, executecommand, print_output=True
    )
    df = pd.DataFrame(data)
    df[0] = df[0].apply(lambda x: x.decode("utf-8", "replace"))
    df[1] = df[0].apply(lambda x: x if "////////////" in x[:15] else pd.NA)
    df[1] = df[1].ffill()
    df = df.dropna()
    df = df.copy()
    df[0] = df[0].str.strip()
    df = df.loc[df[0].str.contains(r"^\d+\s+\d+")]
    print(df)

    dfcomplete = df[0].str.split(n=9, expand=True).copy()
    dfcomplete["aa_folder"] = df[1].str.strip().str.strip(":/")
    symlink = dfcomplete[9].str.split(" -> ", regex=False, expand=True)
    df = pd.concat([dfcomplete, symlink], axis=1, ignore_index=True)
    df["aa_fullpath"] = df[10] + "/" + df[11]
    df = df.loc[~((df[9] == ".") | (df[9] == ".."))]
    df.columns = [
        "aa_id",
        "aa_index",
        "aa_rights",
        "aa_links",
        "aa_owner",
        "aa_group",
        "aa_size",
        "aa_date",
        "aa_time",
        "aa_filename_with_symlink",
        "aa_folder",
        "aa_filename",
        "aa_symlink",
        "aa_fullpath",
    ]
    df = df.loc[~(~df.aa_time.str.contains(":") | (df.aa_size.str.contains(",")))]
    df = df.copy()
    df.aa_date = df.aa_date + " " + df.aa_time
    df = df.drop(columns="aa_time").reset_index(drop=True).copy()
    try:
        df.aa_date = pd.to_datetime(df.aa_date)
    except Exception:
        pass
    df = df.filter(list(sorted(df.columns))).fillna(pd.NA)
    try:
        df["aa_filename"] = df["aa_filename"].astype("string")
    except Exception:
        pass
    try:
        df["aa_folder"] = df["aa_folder"].astype("category")
    except Exception:
        pass
    try:
        df["aa_fullpath"] = df["aa_fullpath"].astype("string")
    except Exception:
        pass
    try:
        df["aa_size"] = df["aa_size"].astype("Int64")
    except Exception:
        pass
    try:
        df["aa_index"] = df["aa_index"].astype("Int64")
    except Exception:
        pass
    try:
        df["aa_rights"] = df["aa_rights"].astype("category")
    except Exception:
        pass
    try:
        df["aa_links"] = df["aa_links"].astype("Int64")
    except Exception:
        pass
    try:
        df["aa_owner"] = df["aa_owner"].astype("category")
    except Exception:
        pass
    try:
        df["aa_group"] = df["aa_group"].astype("category")
    except Exception:
        pass
    try:
        df["aa_id"] = df["aa_id"].astype("Int64")
    except Exception:
        pass

    df["ff_pull_file"] = df.apply(
        lambda x: FlexiblePartial(
            pull_adb_file,
            "()",
            True,
            folder_on_device=x.aa_folder,
            fullpath_on_device=x.aa_fullpath,
            adb_path=adb_path,
            serialnumber=device,
        ),
        axis=1,
    )

    df["ff_remove_file"] = df.apply(
        lambda x: FlexiblePartial(
            remove_file,
            "()",
            True,
            fullpath_on_device=x.aa_fullpath,
            adb_path=adb_path,
            serialnumber=device,
        ),
        axis=1,
    )

    df["ff_pull_file_cat"] = df.apply(
        lambda x: FlexiblePartial(
            pull_with_cat,
            "()",
            True,
            folder_on_device=x.aa_folder,
            fullpath_on_device=x.aa_fullpath,
            adb_path=adb_path,
            device_serial=device,
        ),
        axis=1,
    )

    return df


def pd_add_adb_to_df():
    pd.Q_adb_to_df = get_folder_df
