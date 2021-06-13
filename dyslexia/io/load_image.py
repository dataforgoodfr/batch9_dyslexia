from typing import Union, IO
from pathlib import Path
from PIL import Image, ExifTags
import cv2
import numpy as np
import requests


def crop_black_border(img):
    tmp = img.copy()

    if len(img.shape) == 3:
        tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(tmp, 1, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[0]

    x, y, w, h = cv2.boundingRect(cnt)
    crop = img[y:y + h, x:x + w]

    return crop


def load_image(fpath: Union[str, IO, Path]):
    image = Image.open(fpath)

    # Find rotation from source
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break

    exif = image._getexif()

    # The orientation of the camera relative to the scene, when the image was captured.
    # 3 = Rotate 180 CW
    # 6 = Rotate 90 CW (or 270 ACW)
    # 8 = Rotate 270 CW (or 90 ACW)
    # OpenCV rotate images by default using Anti-Clockwise direction

    crop_border = False
    if exif is not None:

        if exif[orientation] == 3:
            image = image.transpose(Image.ROTATE_180)
        elif exif[orientation] == 6:
            image = image.transpose(Image.ROTATE_270)
            crop_border = True
        elif exif[orientation] == 8:
            image = image.transpose(Image.ROTATE_90)
            crop_border = True

    # Convert as np.array so that it's usable with cv2
    image = np.array(image)

    # Only crop if rotate 270 or 90
    if crop_border:
        image = crop_black_border(image)

    return image


def load_image_from_url(url: str) -> np.ndarray:
    req = requests.get(url, stream=True)
    img = Image.open(req.raw)

    img = np.array(img)

    return img

def load_image_from_string(fpath):
    if fpath.startswith('http'):
        image_orig = load_image_from_url(fpath)
    else:
        image_orig = load_image(fpath)

    return image_orig