import random
import subprocess
from charchef import aa_convert_utf8_to_ascii_
from subprocess_print_and_capture import (
    execute_subprocess_multiple_commands_with_timeout_bin,
)

androidkeys = {
    "0": "KEYCODE_0",
    "1": "KEYCODE_1",
    "2": "KEYCODE_2",
    "3": "KEYCODE_3",
    "4": "KEYCODE_4",
    "5": "KEYCODE_5",
    "6": "KEYCODE_6",
    "7": "KEYCODE_7",
    "8": "KEYCODE_8",
    "9": "KEYCODE_9",
    "A": "KEYCODE_A",
    "'": "KEYCODE_APOSTROPHE",
    "@": "KEYCODE_AT",
    "B": "KEYCODE_B",
    "\\": "KEYCODE_BACKSLASH",
    "C": "KEYCODE_C",
    ",": "KEYCODE_COMMA",
    "D": "KEYCODE_D",
    "E": "KEYCODE_E",
    "=": "KEYCODE_EQUALS",
    "F": "KEYCODE_F",
    "G": "KEYCODE_G",
    "`": "KEYCODE_GRAVE",
    "H": "KEYCODE_H",
    "I": "KEYCODE_I",
    "J": "KEYCODE_J",
    "K": "KEYCODE_K",
    "L": "KEYCODE_L",
    "[": "KEYCODE_LEFT_BRACKET",
    "M": "KEYCODE_M",
    "-": "KEYCODE_MINUS",
    "N": "KEYCODE_N",
    "(": "KEYCODE_NUMPAD_LEFT_PAREN",
    ")": "KEYCODE_NUMPAD_RIGHT_PAREN",
    "O": "KEYCODE_O",
    "P": "KEYCODE_P",
    ".": "KEYCODE_PERIOD",
    "+": "KEYCODE_PLUS",
    "#": "KEYCODE_POUND",
    "Q": "KEYCODE_Q",
    "R": "KEYCODE_R",
    "]": "KEYCODE_RIGHT_BRACKET",
    "S": "KEYCODE_S",
    ";": "KEYCODE_SEMICOLON",
    "/": "KEYCODE_SLASH",
    "*": "KEYCODE_STAR",
    "T": "KEYCODE_T",
    "U": "KEYCODE_U",
    "V": "KEYCODE_V",
    "W": "KEYCODE_W",
    "X": "KEYCODE_X",
    "Y": "KEYCODE_Y",
    "Z": "KEYCODE_Z",
}
escapeddict = {
    "(": r"\(",
    ")": r"\)",
    "<": r"\<",
    ">": r"\>",
    "|": r"\|",
    ";": r"\;",
    "&": r"\&",
    "*": r"\*",
    "\\": r"\\",
    "~": r"\~",
    '"': r"\"",
    "'": r"\'",
    " ": r"\ ",
}


def execute_multicommands_adb_shell(
    adb_path,
    device_serial,
    subcommands: list,
    exit_keys: str = "ctrl+x",
    print_output=False,
    timeout=None,
    use_root=False,
):
    if not isinstance(subcommands, list):
        subcommands = [subcommands]
    if use_root:
        subcommands.insert(0, "su")
    return execute_subprocess_multiple_commands_with_timeout_bin(
        cmd=f"{adb_path} -s {device_serial} shell",
        subcommands=subcommands,
        exit_keys=exit_keys,
        end_of_printline="",
        print_output=print_output,
        timeout=timeout,
    )


def connect_to_adb(adb_path, deviceserial):
    _ = subprocess.run(f"{adb_path} start-server", capture_output=True, shell=False)
    _ = subprocess.run(
        f"{adb_path} connect {deviceserial}", capture_output=True, shell=False
    )


def convert_text_each_letter(
    text, delay=(0.01, 0.2), respect_german_letters=True, debug=False
):
    bigc1 = aa_convert_utf8_to_ascii_(
        str_=text,
        preprocessing_functions=(
            "8x_3_lower_case_escaped",
            "8x_3_upper_case_escaped",
            "8u_4_upper_case_escaped",
            "8u_4_lower_case_escaped",
            "8x_69_upper_case_escaped",
            "8x_69_lower_case_escaped",
            "8n_escaped",
            "8wrong_chars",
            "8zerox_unescaped_lower",
            "8zerox_unescaped_upper",
        ),
        preprocessing_function_non_printable=(
            "substitute_allcontrols_s",
            "substitute_allcontrols",
            "substitute_allcontrols2",
            "substitute_allcontrols2_s",
            "substitute_allcontrols3",
            "substitute_allcontrols3_s",
        ),
        respect_german_letters=respect_german_letters,
    )
    alltext = []
    for ini, k in enumerate(bigc1):
        if ini != 0:
            alltext.append("input keyevent 66")
        for ini2, kk in enumerate(k):
            delayadb = random.uniform(*delay)
            delayadb = round(delayadb, 3)
            alltext.append(f"sleep {delayadb}")
            try:
                alltext.append(f"input text {escapeddict[kk]}")
            except Exception:
                alltext.append(f"input text {kk}")
    if debug:
        for a in alltext:
            print(a)
    return alltext


def convert_text(text, respect_german_letters=True, debug=False):
    bigc1 = aa_convert_utf8_to_ascii_(
        str_=text,
        preprocessing_functions=(
            "8x_3_lower_case_escaped",
            "8x_3_upper_case_escaped",
            "8u_4_upper_case_escaped",
            "8u_4_lower_case_escaped",
            "8x_69_upper_case_escaped",
            "8x_69_lower_case_escaped",
            "8n_escaped",
            "8wrong_chars",
            "8zerox_unescaped_lower",
            "8zerox_unescaped_upper",
        ),
        preprocessing_function_non_printable=(
            "substitute_allcontrols_s",
            "substitute_allcontrols",
            "substitute_allcontrols2",
            "substitute_allcontrols2_s",
            "substitute_allcontrols3",
            "substitute_allcontrols3_s",
        ),
        respect_german_letters=respect_german_letters,
    )
    alltext = []
    for ini, k in enumerate(bigc1):
        escapedtext = ""
        if ini != 0:
            alltext.append("input keyevent 66")
        for ini2, kk in enumerate(k):
            try:
                escapedtext += escapeddict[kk]
            except Exception:
                escapedtext += kk
        alltext.append(f"input text {escapedtext}")
    if debug:
        for a in alltext:
            print(a)
    return alltext


class ADBInputEscaped:
    def __init__(self, adb_path, deviceserial):
        self.adb_path = adb_path
        self.deviceserial = deviceserial
        self.debug = False

    def connect_to_device(self):
        connect_to_adb(self.adb_path, self.deviceserial)
        return self

    def escape_text_and_send(
        self, text, respect_german_letters=True, exit_keys="ctrl+x"
    ):
        text = convert_text(
            text.replace("\t", "    ").splitlines(),
            respect_german_letters=respect_german_letters,
            debug=self.debug,
        )
        execute_multicommands_adb_shell(
            self.adb_path,
            self.deviceserial,
            text,
            exit_keys=exit_keys,
            print_output=False,
            timeout=None,
            use_root=False,
        )
        return self

    def escape_text_and_send_with_delay(
        self, text, delay=(0.01, 0.2), respect_german_letters=True, exit_keys="ctrl+x"
    ):
        text = convert_text_each_letter(
            text.replace("\t", "    ").splitlines(),
            delay=delay,
            respect_german_letters=respect_german_letters,
            debug=self.debug,
        )

        execute_multicommands_adb_shell(
            self.adb_path,
            self.deviceserial,
            text,
            exit_keys=exit_keys,
            print_output=False,
            timeout=None,
            use_root=False,
        )
        return self

    def activate_debug(self):
        self.debug = True
        return self

    def deactivate_debug(self):
        self.debug = False
        return self

