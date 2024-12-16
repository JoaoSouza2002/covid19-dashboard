import os
import sys
import pandas as pd
import cv2
import pathos
from callpyfile import run_py_file
from a_cv_imwrite_imread_plus import open_image_in_cv
here = os.path.abspath(os.path.dirname(__file__))
executefile = os.path.normpath(os.path.join(here, "call3.py"))


def tesser2df(
    pics,
    language="eng",
    pandas_kwargs=dict((("on_bad_lines", "warn"),)),
    tesser_args=(),
    cpus=4,
    tesser_path=r"C:\Program Files\Tesseract-OCR\tesseract.exe",
):
    allpics = [
        (
            pandas_kwargs,
            tesser_path,
            language,
            tesser_args,
            y,
            open_image_in_cv(x),
        )
        for y, x in enumerate(pics)
    ]

    dfa = run_py_file(
        variables={"imagelist": allpics, "cpus": cpus},
        pyfile=executefile,
        activate_env_command="",
        pythonexe=sys.executable,
        raise_exception=False,
    )
    return [x for x in zip(dfa, pics)]


