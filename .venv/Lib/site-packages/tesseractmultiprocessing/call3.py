import io
import cv2
import pandas as pd
import subprocess
import tempfile
from a_cv_imwrite_imread_plus import open_image_in_cv
from callpyfile import to_stdout
from pathos.multiprocessing import ProcessingPool as Pool
import time

stdcols = [
    "level",
    "page_num",
    "block_num",
    "par_num",
    "line_num",
    "word_num",
    "left",
    "top",
    "width",
    "height",
    "conf",
    "text",
    "img_index",
]


def convert_np_array_to_png(img):
    img = open_image_in_cv(img)
    is_success, buffer = cv2.imencode(".png", img)
    io_buf = io.BytesIO(buffer)
    return io_buf.getvalue()


def get_dataframe(index_and_image):
    (
        pandas_config,
        tesser_path,
        tesser_language,
        tesseract_args,
        img_index,
        img,
    ) = index_and_image

    try:
        output_data = convert_np_array_to_png(img)
        with tempfile.SpooledTemporaryFile() as image_file:
            image_file.write(output_data)
            image_file.seek(0)

            args = [
                tesser_path,
                "-c",
                "tessedit_create_tsv=1",
                *tesseract_args,
                "-l",
                tesser_language,
                "-",
                "stdout",
            ]

            result = subprocess.run(
                args, stdin=image_file, capture_output=True, text=True
            )
        output_text = result.stdout
        df = pd.read_csv(io.StringIO(output_text), sep="\t", **pandas_config)
        df["img_index"] = img_index

        df["middle_x"] = df.left + (df.width // 2)
        df["middle_y"] = df.top + (df.height // 2)
        df["conf"] = df["conf"].astype("Float64")
        df["start_x"] = df.left
        df["start_y"] = df.top
        df["end_x"] = df.left + df.width
        df["end_y"] = df.top + df.height

        return df
    except Exception as fe:
        try:
            return pd.DataFrame(columns=stdcols)

        except Exception:
            return pd.DataFrame()


@to_stdout(kill_if_exception=True)
def start_tesseract_rec():
    pool = Pool(nodes=cpus)
    res = pool.amap(get_dataframe, imagelist)
    while not res.ready():
        time.sleep(0.001)
    allb = res.get()
    return allb


if __name__ == "__main__":
    start_tesseract_rec()
