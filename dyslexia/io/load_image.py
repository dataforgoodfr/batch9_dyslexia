from PIL import Image, ExifTags
import cv2
import numpy as np


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

    exif = image._getexif()
    
    # The orientation of the camera relative to the scene, when the image was captured.
    # 3 = Rotate 180 CW
    # 6 = Rotate 90 CW (or 270 ACW)
    # 8 = Rotate 270 CW (or 90 ACW)
    # OpenCV rotate images by default using Anti-Clockwise direction
    if exif[orientation] == 3:
        image=image.transpose(Image.ROTATE_180)
    elif exif[orientation] == 6:
        image=image.transpose(Image.ROTATE_270)
    elif exif[orientation] == 8:
        image=image.transpose(Image.ROTATE_90)

    # Convert as np.array so that it's usable with cv2
    image = np.array(image)

    # Remove black border after rotation
    if orientation > 0:
        image = crop_black_border(image)

    return image
