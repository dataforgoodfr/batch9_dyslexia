from PIL import Image, ExifTags
import cv2
import numpy as np


def fix_orientation(orientation):
    if orientation < 45:
        return 0
    elif orientation < 135:
        return 90
    elif orientation < 225:
        return 180
    elif orientation < 315:
        return 270
    return 0


def crop_black_border(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[0]

    x, y, w, h = cv2.boundingRect(cnt)
    crop = img[y:y + h, x:x + w]

    return crop


def load_image(fpath: str):
    image = Image.open(fpath)

    # Find rotation from source
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    # Fix rotation so that it should be 0, 90, 180 or 270
    orientation = fix_orientation(orientation)

    exif = image._getexif()
    # Rotate image
    image = image.rotate(orientation)

    # Convert as np.array so that it's usable with cv2
    image = np.array(image)

    # Remove black border after rotation
    if orientation > 0:
        image = crop_black_border(image)

    return image