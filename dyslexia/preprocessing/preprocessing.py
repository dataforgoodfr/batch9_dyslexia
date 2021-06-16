import cv2
import numpy as np
import imutils
from skimage.filters import laplace
from skimage.transform import resize
from sklearn.svm import SVC
import joblib


def rgb2gray(rgb: np.ndarray):
    """Converts an TGB image (shape (w, h, 3))
    as grayscale image (shape (w, h)) 

    Parameters
    ----------
    rgb : np.ndarray
        Image as RGB, shape = (w, h, 3)

    Returns
    -------
    np.ndarray
        Image as grayscale, shape = (w, h)
    """
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])


def rotate_img(image: np.ndarray, angle: float):
    """Rotates an image using an angle

    Parameters
    ----------
    image : np.ndarray
        Source image
    angle : float
        Angle for rotation

    Returns
    -------
    np.ndarray
        Rotated image
    """
    return imutils.rotate_bound(image, angle)

    # image_center = tuple(np.array(image.shape[1::-1]) / 2)

    # rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)

    # result = cv2.warpAffine(image,
    #                         rot_mat,
    #                         image.shape[1::-1],
    #                         flags=cv2.INTER_LINEAR)

    # return result


def image_to_gray(image: np.ndarray, threshold=False):
    """Update an image to grayscale with
    the possibility to threshold it

    Parameters
    ----------
    image : np.ndarray
        Source image
    threshold : bool, default False
        Whether it uses threshold or not

    Returns
    -------
    np.ndarray
        Updated image
    """
    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.bitwise_not(image)

    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    if threshold:
        thresh = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        return thresh

    return gray


def find_text_angle(image: np.ndarray):
    """Find text angle if the image is not scanned.

    It's recommended that you use theses functions before using this one:

    # ``remove_shadow(image)``
    # ``image_to_gray(image, threshold=True)``


    Inspired by http://felix.abecassis.me/2011/09/opencv-detect-skew-angle/

    Parameters
    ----------
    image : np.ndarray
        Source image

    Returns
    -------
    np.ndarray
        Updated image
    """

    lines = cv2.HoughLinesP(image,
                            rho=1,
                            theta=1 * np.pi / 180,
                            threshold=100,
                            minLineLength=100,
                            maxLineGap=50)

    angles = list()

    for line in lines:
        line = line[0]
        angle = np.arctan2((line[3] - line[1]), (line[2] - line[0]))
        angles.append(angle)

    # mean angle
    angle = np.mean(angles) * 180 / np.pi

    return angle


def remove_shadow(img: np.ndarray):
    """Remove shadow on an image

    Code from https://stackoverflow.com/questions/44752240/how-to-remove-shadow-from-scanned-images-using-opencv

    Parameters
    ----------
    img : np.ndarray
        [description]

    Returns
    -------
    np.ndarray
        Updated image without shadow
    """
    rgb_planes = cv2.split(img)

    # result_planes = []
    result_norm_planes = []

    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((9,9), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)

        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img,
                                 None,
                                 alpha=0,
                                 beta=255,
                                 norm_type=cv2.NORM_MINMAX,
                                 dtype=cv2.CV_8UC1)

        # result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    # result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)

    return result_norm




def alter_brightness(img, value=30):

    if len(img.shape) == 3:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
    else:
        v = img

    # Increase brightness
    if value >= 0:
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
    # Reduce brightness
    else:
        lim = 0 - value
        v[v < lim] = 0
        v[v >= lim] -= -(value)

    if len(img.shape) == 3:
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    else:
        img = v
    
<<<<<<< HEAD
    return img




def is_image_blurry(img):
    """ Classifier for blurry images """
    model = joblib.load('C:/users/arthu/travail/dataforgood/nathan_dyslexia/batch9_dyslexia/dyslexia/preprocessing/blur_detection_model.sav')
    img = remove_shadow(img)
    
    img = image_to_gray(img, threshold=True)
    img = resize(img, (400, 600))
    edge_laplace = laplace(img, ksize=3)
    variance_laplace= np.var(edge_laplace)
    maximum_laplace = np.amax(edge_laplace)
    entry = [[maximum_laplace,variance_laplace]]
    return 1-model.predict(entry)[0]
=======
    return img
>>>>>>> main
