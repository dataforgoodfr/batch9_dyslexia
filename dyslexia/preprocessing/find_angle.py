from cmath import rect, phase
from math import radians, degrees
import cv2
import numpy as np

from dyslexia import preprocessing


def mean_angle(deg):
    return degrees(phase(sum(rect(1, radians(d)) for d in deg) / len(deg)))


def reject_outliers(values, m=2):
    values = np.array(values)

    return values[abs(values - mean_angle(values)) < m * np.std(values)]


def compute_rotation_angle(image):
    """Find best text angle direction

    It's recommended that you use theses functions before using this one:

    # ``remove_shadow(image)``
    # ``image_to_gray(image, threshold=True)``
    """
    gray = 255 - image

    # Apply threshold to binarize image
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thresh = 255 - thresh

    # apply close to connect the white areas
    kernel = np.ones((5, 5), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((1, 9), np.uint8)
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
    kernel = np.ones((9, 1), np.uint8)
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

    # Use HoughLines method to find lines
    lines = cv2.HoughLinesP(morph,
                            rho=1,
                            theta=1 * np.pi / 180,
                            threshold=100,
                            minLineLength=100,
                            maxLineGap=50)
    lines = np.reshape(lines, (lines.shape[0], 4))

    angles = []
    for x1, y1, x2, y2 in lines:  #[:1000]:
        # get angle
        angle = np.arctan2((y2 - y1), (x2 - x1))

        # To degrees
        angle = angle * 180 / np.pi

        # Since we don't know where is the top of
        # the picture then we just want the direction
        if angle < 0:
            angle = -angle

        # Multiply angle by 2 so that mean on degrees work
        # for line direction only
        angles.append(angle * 2)

    # Reject outliers (like paper border lines)
    angles = reject_outliers(angles, m=1)

    # Divides mean by 2 to retrieves direction
    angle = mean_angle(angles) / 2

    return angle


def find_best_rotation_angle(image: np.ndarray, threshold=1):
    """Find best text angle direction

    It's recommended that you use theses functions before using this one:

    # ``remove_shadow(image)``
    # ``image_to_gray(image, threshold=True)``
    
    Apply this algorithm to find the best angle.
    
    #. use ``compute_rotation_angle()`` to get first angle detected
    #. if angle is close to 180 or 0 then it's already good
    #. else rotated image by angle
    #. Use this image to use again ``compute_rotation_angle()``
    #. if angle is close to 180 or 0 then use this angle
    #. do the same for but with minus first angle found
    #. If neither angles are close enough then use the closest from 180 or 0    
    
    Parameters
    ----------
    image : np.ndarray
        Source image
    threshold : int, default 1
        Distance in degree from horizontal line (180 or 0 degrees)
        to consider an angle to be good

    Returns
    -------
    number:
        Best rotation angle for this image
    """
    angle = compute_rotation_angle(image)

    if abs(angle - 90) > 90 - threshold:
        return angle

    img_rotated = preprocessing.rotate_img(image, angle)
    new_angle1 = compute_rotation_angle(img_rotated)

    if abs(new_angle1 - 90) > 90 - threshold:
        return angle

    img_rotated = preprocessing.rotate_img(image, -angle)
    new_angle2 = compute_rotation_angle(img_rotated)

    if abs(new_angle2 - 90) > 90 - threshold:
        return -angle

    if abs(new_angle1 - 90) > abs(new_angle2 - 90):
        return angle

    return -angle
