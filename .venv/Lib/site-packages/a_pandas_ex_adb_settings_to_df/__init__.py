import re

import regex
from a_pandas_ex_text_compare import pd_add_text_difference

pd_add_text_difference()
import ujson
from a_pandas_ex_xml2df import xml_to_df
from flexible_partial import FlexiblePartialOwnName
from list_all_files_recursively import get_folder_file_complete_path
import pandas as pd

from a_pandas_ex_read_sql import pd_add_read_sql_file

pd_add_read_sql_file()
from a_pandas_ex_plode_tool import pd_add_explode_tools

pd_add_explode_tools()
from a_pandas_ex_adb_to_df import pd_add_adb_to_df
from a_pandas_ex_adb_to_df import execute_subprocess_multiple_commands_with_timeout_bin

pd_add_adb_to_df()


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


def get_sed_preview_command(adb_path, deviceserial, str_, file, inplace):
    aa_snippet = str_
    fullpath_on_device = file

    if not inplace:
        cmd = f"""su -c 'test=$(echo "{aa_snippet}"); echo $( sed s~"$test"~'{{replacement}}'~g {fullpath_on_device})'"""

    else:
        cmd = f"""su -c 'test=$(echo "{aa_snippet}"); echo $( sed -i s~"$test"~'{{replacement}}'~g {fullpath_on_device})'"""

    return FlexiblePartialOwnName(
        get_sed_preview, cmd, True, adb_path, deviceserial, str_, file, inplace
    )


def pull_with_cat(
    adb_path,
    device_serial,
    fullpath_on_device,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    command = f"""su -- cat {fullpath_on_device}"""
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
    return filax


def get_sed_preview(
    adb_path,
    deviceserial,
    str_,
    file,
    inplace,
    replacement,
    exit_keys="ctrl+x",
    print_output=True,
    timeout=None,
):
    aa_snippet = str_
    fullpath_on_device = file
    replacement = f'"{replacement}"'.replace('"', """\\\"""")

    if not inplace:
        cmd = f"""su -c 'test=$(echo "{aa_snippet}"); echo $( sed s~"$test"~'{replacement}'~g {fullpath_on_device})'"""

    else:
        cmd = f"""su -c 'test=$(echo "{aa_snippet}"); echo $( sed -i s~"$test"~'{replacement}'~g {fullpath_on_device})'"""

    caddu = pull_with_cat(adb_path, deviceserial, file)
    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[cmd],
        exit_keys=exit_keys,
        print_output=print_output,
        timeout=timeout,
    )
    return pd.Q_text_difference_to_df(
        text1=b"".join(xx).decode("utf-8", "ignore"),
        text2=b"".join(caddu).decode("utf-8", "ignore"),
        encoding="utf-8",
    )


def parse_config_files(
    adb_path: str,
    deviceserial: str,
    save_in_folder: str,
    folder: str = "data/",
    with_sed_columns: bool = False,
) -> pd.DataFrame:
    df = pd.Q_adb_to_df(device=deviceserial, adb_path=adb_path, folder=folder)
    df.loc[
        df.aa_filename.str.contains(
            r"\.(?:json|xml|db)$", regex=True, flags=re.I, na=False
        )
        & (df.aa_size > 0)
    ].ff_pull_file_cat.apply(lambda x: x(save_in_folder))
    allfiles = get_folder_file_complete_path(save_in_folder)
    daa = []

    for x in allfiles:

        if x.ext.lower() == ".xml":
            try:
                xmldf = xml_to_df(x.path, add_xpath_and_snippet=True)
                xmldf["aa_file"] = x.path
                daa.append(xmldf.reset_index(drop=False).copy())
            except Exception as fe:
                print(f"{x.path} Could not be read!", end="\r")
                print(fe, end="\r")
                print(
                    "Usually, you can ignore the error messages. There are always some empty files on a Android device.",
                    end="\r",
                )

    daa1 = pd.concat(daa).copy()

    daa2 = []
    for x in allfiles:

        if x.ext.lower() == ".db":
            try:
                sqldf = pd.Q_read_sql(x.path)
                for key, item in sqldf.items():
                    newfa = pd.Q_AnyNestedIterable_2df(item)
                    newfa["aa_file"] = x.path
                    newfa["aa_xpath"] = pd.NA
                    newfa["aa_snippet"] = pd.NA

                    daa2.append(newfa.copy())
            except Exception as fe:
                print(f"{x.path} Could not be read!", end="\r")
                print(fe, end="\r")
    daa22 = pd.concat(daa2).copy()
    dafa = pd.concat([daa1, daa22], ignore_index=True)

    jstu = []
    for x in allfiles:

        if x.ext.lower() == ".json":
            try:
                with open(x.path, mode="rb") as f:
                    datas = f.read()
                ba = pd.Q_AnyNestedIterable_2df(ujson.loads(datas))
                ba["aa_file"] = x.path
                ba["aa_xpath"] = pd.NA
                ba["aa_snippet"] = pd.NA
                jstu.append(ba.copy())
            except Exception as fe:
                print(f"{x.path} Could not be read!", end="\r")
                print(fe, end="\r")
                continue

    dfj = pd.concat(jstu, ignore_index=True)
    dafa = pd.concat([dafa, dfj], ignore_index=True).copy()

    dafa["aa_file_android"] = dafa.aa_file.str.replace(
        save_in_folder, "", regex=False
    ).str.replace("\\", "/", regex=False)

    if with_sed_columns:

        dafa.aa_snippet = dafa.aa_snippet.apply(
            lambda x: regex.sub(r"\s*/>\s*$", "", x.rstrip())
            .replace('"', """\\\"""")
            .strip()
            if isinstance(x, str)
            else pd.NA
        )

        dafa["aa_sed_preview"] = dafa.apply(
            lambda x: get_sed_preview_command(
                adb_path, deviceserial, x.aa_snippet, x.aa_file_android, inplace=False
            ),
            axis=1,
        )
        dafa["aa_sed_replace"] = dafa.apply(
            lambda x: get_sed_preview_command(
                adb_path, deviceserial, x.aa_snippet, x.aa_file_android, inplace=True
            ),
            axis=1,
        )

    dafa = dafa.drop(columns=[x for x in dafa.columns if str(x).startswith("level_")])
    dafa = dafa.ds_horizontal_explode("aa_all_keys")
    dafa.columns = [
        f'level_{x.replace("aa_all_keys_", "")}'
        if str(x).startswith("aa_all_keys_")
        else x
        for x in dafa.columns
    ]
    return dafa.copy()

def pd_add_adb_settings_to_df():
    pd.Q_adb_settings_to_df = parse_config_files

