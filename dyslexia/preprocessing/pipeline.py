from dyslexia import preprocessing 
from dyslexia.src.french_words import french_words
from dyslexia import ocr
from dyslexia.io import load_image

def count_nb_french_words(txt):
    cnt = 0
    
    for w in txt.lower().split():
        if w in set(french_words):
            cnt += 1
            
    return cnt


def preprocess_image(image):
    image_no_shadow = preprocessing.remove_shadow(image)
    
    image_gray = preprocessing.image_to_gray(image_no_shadow, threshold=True)

    angle = preprocessing.find_best_rotation_angle(image_gray)
    
    image_fixed = preprocessing.rotate_img(image_gray, angle=angle)
    
    return image_fixed


def pipeline(fpath):
    image_orig = load_image(fpath)
    image_prep = preprocess_image(image_orig)
    
    # Since we don't know the real angle of the image
    # Check with find angle
    res = ocr.extract_data_from_image(image_prep, lang='fra')
    txt, bboxes = ocr.format_pytesseract_dict_results(res)
    nb_fr_words = count_nb_french_words(' '.join(txt))
    
    # Then check for rotated 180 degrees image
    image_prep_180 = preprocessing.rotate_img(image_prep, 180)
    res_180 = ocr.extract_data_from_image(image_prep_180, lang='fra')
    txt_180, bboxes_180 = ocr.format_pytesseract_dict_results(res_180)
    nb_fr_words_180 = count_nb_french_words(' '.join(txt_180))
    
    if nb_fr_words > nb_fr_words_180:
        return txt, bboxes
    elif nb_fr_words_180 > nb_fr_words:
        return txt_180, bboxes_180
    
    # Nothing found
    if nb_fr_words == 0:
        raise Exception('No text found')

    return txt, bboxes


def get_results(fpath, out='json'):

    txt, bboxes = pipeline(fpath)

    res = {
        'paragraphs': txt,
        'bboxes': bboxes
    }

    if out == 'json':
        return res

    return txt, bboxes