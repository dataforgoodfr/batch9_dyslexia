from dyslexia.app import pipeline
from dyslexia.app.errors import NoTextFoundError, ImageBlurryError

<<<<<<< HEAD

def get_results(fpath: str) -> dict:
=======
from dyslexia.io import load_image_from_string
from PIL import Image
from io import BytesIO
import numpy as np


def load_image_into_numpy_array(data):
    return np.array(Image.open(BytesIO(data)))


def get_results(data) -> dict:
>>>>>>> main
    """Executes the pipeline function that requires a valid path

    If the pipeline is executed successfully then it returns
    a dictionnary with 2 keys : 'paragraphs' that contains a list of text and
<<<<<<< HEAD
    'bboxes' containing coordinates (x1, y1, x2, y2) for each paragraph
=======
    'bboxes' containing coordinates (x1,y1,w,h) for each paragraph
>>>>>>> main

    Else there are 3 possibles errors :
    1. The image is blurry
    2. No french text found in the output
    3. Unknown error

    Parameters
    ----------
<<<<<<< HEAD
    fpath : str
        Valid path to an image
=======
    data: str or uploaded file
        input data from API call it can be a string (url or path to file)
        or the stream of the uploaded image
>>>>>>> main

    Returns
    -------
    dict
        dictionnary with 2 keys : 'paragraphs' that contains a list of text and
<<<<<<< HEAD
        'bboxes' containing coordinates (x1, y1, x2, y2) for each paragraph
    """

    try:
        txt, bboxes = pipeline(fpath)

    except ImageBlurryError as e:
        return {'error': {'code': 'IMAGE_BLURRY', 'message': str(e)}}
        
=======
        'bboxes' containing coordinates (x1,y1,w,h) for each paragraph
    """
    try:
        if isinstance(data, str):
            img = load_image_from_string(data)
        else:
            img = load_image_into_numpy_array(data)

        txt, bboxes = pipeline(img)

    except ImageBlurryError as e:
        return {'error': {'code': 'IMAGE_BLURRY', 'message': str(e)}}

>>>>>>> main
    except NoTextFoundError as e:
        return {'error': {'code': 'NO_TEXT_FOUND', 'message': str(e)}}

    except Exception as e:
        return {'error': {'code': 'UNKNOWN_ERROR', 'message': str(e)}}

<<<<<<< HEAD

=======
>>>>>>> main
    res = {'paragraphs': txt, 'bboxes': bboxes}

    return res