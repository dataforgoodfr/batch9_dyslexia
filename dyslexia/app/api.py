from dyslexia.app import pipeline
from dyslexia.app.errors import NoTextFoundError, ImageBlurryError


def get_results(fpath: str) -> dict:
    """Executes the pipeline function that requires a valid path

    If the pipeline is executed successfully then it returns
    a dictionnary with 2 keys : 'paragraphs' that contains a list of text and
    'bboxes' containing coordinates (x1, y1, x2, y2) for each paragraph

    Else there are 3 possibles errors :
    1. The image is blurry
    2. No french text found in the output
    3. Unknown error

    Parameters
    ----------
    fpath : str
        Valid path to an image

    Returns
    -------
    dict
        dictionnary with 2 keys : 'paragraphs' that contains a list of text and
        'bboxes' containing coordinates (x1, y1, x2, y2) for each paragraph
    """

    try:
        txt, bboxes = pipeline(fpath)

    except ImageBlurryError as e:
        return {'error': {'code': 'IMAGE_BLURRY', 'message': str(e)}}
        
    except NoTextFoundError as e:
        return {'error': {'code': 'NO_TEXT_FOUND', 'message': str(e)}}

    except Exception as e:
        return {'error': {'code': 'UNKNOWN_ERROR', 'message': str(e)}}


    res = {'paragraphs': txt, 'bboxes': bboxes}

    return res