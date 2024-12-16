from threading import Thread
from typing import Union
import numpy as np
import cv2
from time import sleep


def imshow_thread(
    image: Union[list, np.ndarray],
    window_name: str = "",
    sleep_time: Union[float, int, None] = None,
    quit_key: str = "q",
) -> None:
    r"""
    Usage:

    import glob
    import os
    from z_imshow import add_imshow_thread_to_cv2 #if you saved this file as z_imshow.py
    add_imshow_thread_to_cv2() #monkey patching
    import cv2
    image_background_folder=r'C:\yolovtest\backgroundimages'
    pics=[cv2.imread(x) for x in glob.glob(f'{image_background_folder}{os.sep}*.png')]
    cv2.imshow_thread( image=pics[0], window_name='screen1',sleep_time=None, quit_key='q') #single picture
    cv2.imshow_thread( image=pics, window_name='screen1',sleep_time=.2, quit_key='e') #sequence of pics like a video clip

        Parameters:
            image: Union[list, np.ndarray]
                You can pass a list of images or a single image
            window_name: str
                Window title
                (default = "")
            sleep_time: Union[float, int, None] = None
                Useful if you have an image sequence.
                If you pass None, you will have to press the quit_key to continue
                (default = None)
            quit_key: str = "q"
                key to close the window
        Returns:
            None

    """
    t = Thread(target=_cv_imshow, args=(image, window_name, sleep_time, quit_key))
    t.start()


def _cv_imshow(
    cvimages: Union[list, np.ndarray],
    title: str = "",
    sleep_time: Union[float, int, None] = None,
    quit_key: str = "q",
) -> None:

    if not isinstance(cvimages, list):
        cvimages = [cvimages]

    if sleep_time is not None:
        for cvimage in cvimages:
            cv2.imshow(title, cvimage)
            if cv2.waitKey(1) & 0xFF == ord(quit_key):
                break
            sleep(sleep_time)
    else:
        for cvimage in cvimages:
            cv2.imshow(title, cvimage)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            cv2.waitKey(1)
    cv2.destroyAllWindows()


def add_imshow_thread_to_cv2():
    cv2.imshow_thread = imshow_thread  # cv2 monkey patching
    # You can also use imshow_thread(window_name, image, sleep_time=None)
    # if you dont like monkey patches
