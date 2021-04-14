from dyslexia import preprocessing
from dyslexia.io import load_image
from dyslexia.ocr import extract_text_from_image
import pathlib
import cv2
from PIL import Image
import numpy as np

in_path = pathlib.Path("../data/images/")
image_paths = in_path.glob("*.jpeg")

out_path = pathlib.Path("../data/hypothesis_preprocessing/")
out_path.mkdir(exist_ok=True)

for image_path in image_paths:
    print(image_path)

    image_orig = Image.open(image_path)
    image_orig = np.array(image_orig)

    image_no_shadow = preprocessing.remove_shadow(image_orig)
    image_gray = preprocessing.image_to_gray(image_no_shadow, threshold=True)
    image_gray = image_gray.max() - image_gray

    cv2.imwrite(image_path.name, image_gray)

    result = extract_text_from_image(image_gray)

    with open(out_path / f"{image_path.stem}.txt", "w") as f:
        f.write(result)
