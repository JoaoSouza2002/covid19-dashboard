### Solution for the "window - not responding" problem with cv2.imshow()

```python
pip install a-cv2-imshow-thread
```

```python
    Usage:

    import glob
    import os
    from a_cv2_imshow_thread import add_imshow_thread_to_cv2 
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
```
