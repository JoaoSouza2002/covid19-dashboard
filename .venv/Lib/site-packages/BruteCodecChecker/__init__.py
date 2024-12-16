import os, codecs, encodings
from collections import OrderedDict
from typing import Union
from cprinter import TC
from input_timeout import InputTimeout


class CodecChecker:
    def __init__(self):
        self.encodingdict = self.get_codecs()
        self.results = OrderedDict()

    def get_codecs(self):
        dir = encodings.__path__[0]
        codec_names = OrderedDict()
        for filename in os.listdir(dir):
            if not filename.endswith(".py"):
                continue
            name = filename[:-3]
            try:
                codec_names[name] = OrderedDict({"object": codecs.lookup(name)})
            except Exception as Fehler:
                pass
        return codec_names

    def try_open_file(self, path: str, readlines: int = 0):
        self.results = OrderedDict()
        results = OrderedDict()
        if readlines == 0:
            for key, item in self.encodingdict.items():
                results[key] = {"strict_encoded": [], "strict_bad": True}

                try:
                    with open(path, encoding=key) as f:
                        data = f.read()
                        results[key]["strict_encoded"].append(data)
                        results[key]["strict_bad"] = False
                except Exception as fe:
                    results[key]["strict_encoded"].append(str(fe))
                    continue
        else:
            for key, item in self.encodingdict.items():
                results[key] = {"strict_encoded": [], "strict_bad": True}

                try:
                    with open(path, encoding=key) as f:
                        for ini, line in enumerate(f.readlines()):
                            if ini == readlines:
                                break
                            results[key]["strict_encoded"].append(line[:-1])
                        results[key]["strict_bad"] = False
                except Exception as fe:
                    results[key]["strict_encoded"].append(str(fe))
                    continue
        self.results = results.copy()
        return self

    def try_convert_bytes(self, variable: bytes):
        self.results = OrderedDict()

        results = OrderedDict()
        modes = ["strict", "ignore", "replace"]
        for key, item in self.encodingdict.items():
            results[key] = {
                "strict_encoded": [],
                "strict_bad": True,
                "ignore_encoded": [],
                "ignore_bad": True,
                "replace_encoded": [],
                "replace_bad": True,
            }
            for mo in modes:
                try:
                    results[key][f"{mo}_encoded"].append(
                        item["object"].decode(variable, mo)
                    )
                    results[key][f"{mo}_bad"] = False
                except Exception as Fe:
                    results[key][f"{mo}_encoded"].append(str(Fe))
        self.results = results.copy()

        return self

    def print_results(
        self, pause_after_interval: Union[int, float] = 0, items_per_interval: int = 0
    ):
        counter = 0
        for key, item in self.results.items():
            if pause_after_interval != 0 and items_per_interval != 0:
                if items_per_interval == counter and counter > 0:
                    i = InputTimeout(
                        timeout=pause_after_interval,
                        input_message=f"Press any key to continue or wait {pause_after_interval} seconds",
                        timeout_message="",
                        defaultvalue="",
                        cancelbutton=None,
                        show_special_characters_warning=None,
                    ).finalvalue
                    counter = 0
            print(
                f'\n\n\n{"Codec".ljust(20)}: {str(TC(key).bg_cyan.fg_black)}'.ljust(100)
            )
            if "strict_bad" in item and "strict_encoded" in item:
                print(f'{"Mode".ljust(20)}: {TC("strict").fg_yellow.bg_black}')

                if item["strict_bad"] is False:
                    if isinstance(item["strict_encoded"][0], tuple):
                        if item["strict_bad"] is False:

                            try:
                                print(
                                    f"""{'Length'.ljust(20)}: {TC(f'''{item['strict_encoded'][0][1]}''').fg_purple.bg_black}\n{'Converted'.ljust(20)}: {TC(f'''{item['strict_encoded'][0][0]}''').fg_green.bg_black}"""
                                )
                            except Exception:
                                print(
                                    f"""Problems during printing! Raw string: {item['strict_encoded'][0][0]!r}"""
                                )

                        if item["strict_bad"] is True:
                            try:
                                print(
                                    f"""{'Length'.ljust(20)}: {TC(f'''{"None"}''').fg_red.bg_black}\n{'Converted'.ljust(20)}: {TC(f'''{item['strict_encoded'][0]}''').fg_red.bg_black}"""
                                )
                            except Exception:
                                print(
                                    f"""Problems during printing! Raw string: {item['strict_encoded'][0][0]!r}"""
                                )
                    if isinstance(item["strict_encoded"][0], str):
                        if item["strict_bad"] is False:
                            itemlen = len("".join(item["strict_encoded"]))
                            concatitem = "\n" + "\n".join(
                                [
                                    f"""Line: {str(y).ljust(14)} {str(f'''{x}''')}"""
                                    for y, x in enumerate(item["strict_encoded"])
                                ]
                            )
                            try:
                                print(
                                    f"""{'Length'.ljust(20)}: {TC(f'''{itemlen}''').fg_purple.bg_black}\n{'Converted'.ljust(20)}: {concatitem}"""
                                )
                            except Exception:
                                print(
                                    f"""Problems during printing! Raw string: {concatitem!r}"""
                                )

                        if item["strict_bad"] is True:
                            concatitem = TC(
                                " ".join(item["strict_encoded"])
                            ).fg_red.bg_black
                            try:
                                print(
                                    f"""{'Length'.ljust(20)}: {TC(f'''{"None"}''').fg_red.bg_black}\n{'Converted'.ljust(20)}: {concatitem}"""
                                )
                            except Exception:
                                print(
                                    f"""Problems during printing! Raw string: {concatitem!r}"""
                                )
                print("")
            if "ignore_bad" in item and "ignore_encoded" in item:
                print(f'{"Mode".ljust(20)}: {TC("ignore").fg_yellow.bg_black}')

                if item["ignore_bad"] is False:
                    if isinstance(item["ignore_encoded"][0], tuple):

                        if item["ignore_bad"] is False:

                            try:
                                print(
                                    f"""{'Length'.ljust(20)}: {TC(f'''{item['ignore_encoded'][0][1]}''').bg_black.fg_lightgrey}\n{'Converted'.ljust(20)}: {TC(f'''{item['ignore_encoded'][0][0]}''').bg_black.fg_lightgrey}"""
                                )
                            except Exception:
                                print(
                                    f"""Problems during printing! Raw string: {item['ignore_encoded'][0][0]!r}"""
                                )
                    # if item["ignore_bad"] is True:
                    #     try:
                    #         print(
                    #             f"""{'Length'.ljust(20)}: {TC(f'''{"None"}''').bg_black.fg_lightgrey}\n{'Converted'.ljust(20)}: {TC(f'''{item['ignore_encoded'][0]}''').bg_black.fg_lightgrey}"""
                    #         )
                    #     except Exception:
                    #         print(
                    #             f"""Problems during printing! Raw string: {item['ignore_encoded'][0][0]!r}"""
                    #         )

                print("")

            if "replace_bad" in item and "replace_encoded" in item:
                print(f'{"Mode".ljust(20)}: {TC("replace").fg_yellow.bg_black}')

                if item["replace_bad"] is False:
                    if isinstance(item["replace_encoded"][0], tuple):

                        if item["replace_bad"] is False:
                            try:
                                print(
                                    f"""{'Length'.ljust(20)}: {TC(f'''{item['replace_encoded'][0][1]}''').bg_black.fg_lightgrey}\n{'Converted'.ljust(20)}: {TC(f'''{item['replace_encoded'][0][0]}''').bg_black.fg_lightgrey}"""
                                )
                            except Exception:
                                print(
                                    f"""Problems during printing! Raw string: {item['replace_encoded'][0][0]!r}"""
                                )
                    # if item["replace_bad"] is True:
                    #     try:
                    #         print(
                    #             f"""{'Length'.ljust(20)}: {TC(f'''{"None"}''').bg_black.fg_lightgrey}\n{'Converted'.ljust(20)}: {TC(f'''{item['replace_encoded'][0]}''').bg_black.fg_lightgrey}"""
                    #         )
                    #     except Exception:
                    #         print(
                    #             f"""Problems during printing! Raw string: {item['replace_encoded'][0][0]!r}"""
                    #         )
            counter = counter + 1

        return self


if __name__ == "__main__":
    teststuff = b"""This is a test! 
    Hi there!
    A little test! """
    testfilename = "test_utf8.tmp"
    with open("test_utf8.tmp", mode="w", encoding="utf-8-sig") as f:
        f.write(teststuff.decode("utf-8-sig"))
    codechecker = CodecChecker()
    codechecker.try_open_file(testfilename, readlines=2).print_results(
        pause_after_interval=1, items_per_interval=10
    )
    codechecker.try_open_file(testfilename).print_results()
    codechecker.try_convert_bytes(teststuff.decode("cp850").encode()).print_results(
        pause_after_interval=1, items_per_interval=10
    )
