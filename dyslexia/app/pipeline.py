from dyslexia import preprocessing
from dyslexia.src.french_words import french_words
from dyslexia import ocr
from dyslexia.io import load_image, load_image_from_url
from dyslexia.app.errors import NoTextFoundError, ImageBlurryError

import numpy as np


def count_nb_french_words(txt: str) -> int:
    """Counts the number of french words based on the french words contains into
    the src.french_words.py file.
    """
    cnt = 0

    for w in txt.lower().split():
        if w in set(french_words):
            cnt += 1

    return cnt


def preprocess_image(image: np.ndarray) -> np.ndarray:
    image_no_shadow = preprocessing.remove_shadow(image)

    darker = preprocessing.alter_brightness(
        image_no_shadow, value=-int(image_no_shadow.mean() * 2 / 3))

    image_gray = preprocessing.image_to_gray(darker, threshold=True)

    angle = preprocessing.find_best_rotation_angle(image_gray)

    image_fixed = preprocessing.rotate_img(image_gray, angle=angle)

    return image_fixed


def pipeline(fpath: str) -> tuple:
    """Executes the pipeline function that requires a valid path

    If the pipeline is executed successfully then it returns
    a tuple:
    - txt that contains a list of text in differents paragraphs
    - bboxes containing coordinates (x1, y1, x2, y2) for each paragraph

    Parameters
    ----------
    fpath : str
        Valid path to an image

    Returns
    -------
    tuple
        txt: list of text in differents paragraphs
        bboxes: coordinates (x1, y1, x2, y2) for each paragraph

    Raises
    ------
    ImageBlurryError
        The image sent by the user is considered to be blurry
    NoTextFoundError
        The OCR model did not found any french word inside the image
    """
    if fpath.startswith('http'):
        image_orig = load_image_from_url(fpath)
    else:
        image_orig = load_image(fpath)

    # Check image blurry
    is_blurry = False
    if is_blurry:
        raise ImageBlurryError('The image sent by the user is considered to be blurry')

    image_prep = preprocess_image(image_orig)

    res = ocr.extract_data_from_image(image_prep, lang='fra')
    txt, bboxes = ocr.format_pytesseract_dict_results(res)
    nb_fr_words = count_nb_french_words(' '.join(txt))

    # Nothing found
    if nb_fr_words == 0:
        raise NoTextFoundError('The OCR model did not found any french word inside the image')

    return txt, bboxes
