# Multiprocessing OCR with Tesseract

## pip install tesseractmultiprocessing

Worth using if you:
1) have plenty of different files 
2) are using numpy

#### Multi: 23.9910116

#### One CPU: 100.61128 #pytesseract


```python
from tesseractmultiprocessing import tesser2df
from a_cv_imwrite_imread_plus import open_image_in_cv
from time import perf_counter

picslinks = [
    r"https://github.com/hansalemaos/screenshots/raw/main/pandsnesteddicthtml.png",
    r"https://github.com/hansalemaos/screenshots/raw/main/cv2_putTrueTypeText_000000.png",
    r"https://github.com/hansalemaos/screenshots/raw/main/cv2_putTrueTypeText_000008.png",
    r"https://github.com/hansalemaos/screenshots/raw/main/cv2_putTrueTypeText_000017.png",
]
picsunique = [open_image_in_cv(x) for x in picslinks]
pics = []
for _ in range(100):
    pics.extend(picsunique)

start = perf_counter()
output = tesser2df(
    pics,
    language="eng",
    pandas_kwargs={"on_bad_lines": "warn"},
    tesser_args=(),
    cpus=5,
    tesser_path=r"C:\Program Files\Tesseract-OCR\tesseract.exe",
)
print(f"Multi: {perf_counter()-start}")


################################################################################

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def st():
    alla = []
    for p in pics:
        alla.append(pytesseract.image_to_data(p))
    return alla


start = perf_counter()
output2 = st()
print(f"One CPU: {perf_counter()-start}")


# Multi: 23.9910116
# One CPU: 100.61128

# output[0]
# Out[4]:
# (    level  page_num  block_num  par_num  ...  start_x  start_y  end_x  end_y
#  0       1         1          0        0  ...        0        0   1465    654
#  1       2         1          1        0  ...      322       64    327    540
#  2       3         1          1        1  ...      322       64    327    540
#  3       4         1          1        1  ...      322       64    327    540
#  4       5         1          1        1  ...      322       64    327    540
#  ..    ...       ...        ...      ...  ...      ...      ...    ...    ...
#  60      5         1         11        1  ...       14      633   1448    644
#  61      2         1         12        0  ...     1445       15   1450    639
#  62      3         1         12        1  ...     1445       15   1450    639
#  63      4         1         12        1  ...     1445       15   1450    639
#  64      5         1         12        1  ...     1445       15   1450    639
#
#  [65 rows x 19 columns],
#  array([[[255, 255, 255],
#          [255, 255, 255],
#          [255, 255, 255],
#          ...,
#          [255, 255, 255],
#          [255, 255, 255],
#          [255, 255, 255]],
#
#         [[255, 255, 255],
#          [255, 255, 255],
#          [255, 255, 255],
#          ...,
#          [255, 255, 255],
#          [255, 255, 255],
#          [255, 255, 255]],

```

