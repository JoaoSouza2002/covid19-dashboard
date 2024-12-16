import itertools
import operator
import os
import shutil
import tempfile
from ast import literal_eval
import io
from functools import partial

import bs4
import regex
import requests
from a_pandas_ex_plode_tool import pd_add_explode_tools
import pandas as pd
from lxml import etree
from nestednop import NestedNop
from xml.etree import ElementTree
from a_pandas_ex_horizontal_explode import pd_add_horizontal_explode

pd_add_horizontal_explode()
pd_add_explode_tools()


class XmlDictConfig(dict):
    """https://stackoverflow.com/questions/2148119/how-to-convert-an-xml-string-to-a-dictionary
    """

    def __init__(self, parent_element):
        if parent_element.items():
            self.updateShim(dict(parent_element.items()))
        for element in parent_element:
            if len(element):
                aDict = XmlDictConfig(element)
                self.updateShim({element.tag: aDict})
            elif element.items():
                elementattrib = element.items()
                if element.text:
                    elementattrib.append((element.tag, element.text))
                self.updateShim({element.tag: dict(elementattrib)})
            else:
                self.updateShim({element.tag: element.text})

    def updateShim(self, aDict):
        for key in aDict.keys():
            if key in self:
                value = self.pop(key)
                if type(value) is not list:
                    listOfDicts = []
                    listOfDicts.append(value)
                    listOfDicts.append(aDict[key])
                    self.update({key: listOfDicts})
                else:
                    value.append(aDict[key])
                    self.update({key: value})
            else:
                self.update({key: aDict[key]})


def get_xpath_and_snippet(dframe):
    def get_xml_snippet(doc, itemtocrawl, configlines):
        alli = list(
            reversed(
                [
                    "//" + regex.sub(r"/(\[\d+)", r"\g<1>", j)
                    for j in list(
                        itertools.accumulate(
                            itemtocrawl,
                            lambda a, b: operator.add(
                                f"{a}/", rf"[{b + 1}]" if isinstance(b, int) else str(b)
                            ),
                        )
                    )
                ]
            )
        )
        for k in alli:
            try:
                target = doc.xpath(k)
                return k, configlines[target[0].sourceline - 1]

            except Exception as fe:
                continue
        return pd.NA, pd.NA

    allsni = []
    dafa = dframe.copy()
    for name, group in dafa.groupby("aa_file"):
        if regex.search(r"\.xml$", name, flags=regex.I) is None:
            continue
        with open(name, mode="rb") as f:
            config = f.read()
        config = config.decode("utf-8", "ignore")
        config = bs4.BeautifulSoup(config, features="xml").prettify()
        configlines = config.splitlines()
        doc = etree.XML(config.encode())

        group2 = group.copy()
        group2["aa_snippet"] = group2.aa_all_keys.apply(
            lambda oo: get_xml_snippet(doc, oo, configlines)
        )
        allsni.append(group2.copy())
    dfia = pd.concat(allsni, ignore_index=True)
    dfia = dfia.ds_horizontal_explode("aa_snippet")
    dfia = dfia.drop(columns="aa_snippet").rename(
        columns={"aa_snippet_0": "aa_xpath", "aa_snippet_1": "aa_snippet"}
    )
    return dfia.drop(columns=["aa_file"])


def load_string(xmlfileorstring):
    if not os.path.exists(xmlfileorstring) and not xmlfileorstring.lower().startswith(
        "http"
    ):
        xmlfileorstring = io.StringIO(xmlfileorstring)
    elif str(xmlfileorstring).lower().startswith("http"):
        tmlp = requests.get(xmlfileorstring).content.decode("utf-8", "ignore")
        xmlfileorstring = io.StringIO(tmlp)
    return xmlfileorstring


def get_tmpfile(suffix=".bin"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = filename.replace("/", os.sep).replace("\\", os.sep)
    tfp.close()
    return filename, partial(os.remove, tfp.name)


def xml_to_dict(file_string_url):
    xmlfileorstring = load_string(file_string_url)

    tree = ElementTree.parse(xmlfileorstring)
    root = tree.getroot()
    xmldict = XmlDictConfig(root)

    nest = NestedNop(xmldict)
    for key, item in nest.iterable_flat.items():
        try:
            item["set_value"](literal_eval(item["get_value"]()))
        except Exception as fe:
            pass
    updatediter = nest.get_updated_iterable()
    return updatediter.copy()


def xml_to_df(file_string_url, add_xpath_and_snippet=False):
    vara = pd.Q_AnyNestedIterable_2df(xml_to_dict(file_string_url)).d_stack()
    if add_xpath_and_snippet:
        if os.path.exists(file_string_url):
            vara["aa_file"] = file_string_url
        else:
            xmlfileorstring = load_string(file_string_url)
            temp, tempre = get_tmpfile(suffix=".xml")
            with open(temp, "w") as fd:
                xmlfileorstring.seek(0)
                shutil.copyfileobj(xmlfileorstring, fd)

            vara["aa_file"] = temp
        vara = get_xpath_and_snippet(dframe=vara)
    return vara


def pd_add_read_xml_files():
    pd.Q_Xml2df = xml_to_df
