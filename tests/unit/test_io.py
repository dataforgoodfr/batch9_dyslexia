from pathlib import Path
from dyslexia import io
import numpy as np

test_path = Path(__file__).resolve().parents[1]


def test_load_image_type():
    image_path = test_path / "data" / "images" / "Sample_0.jpeg"

    image = io.load_image(str(image_path), crop_border=False)

    assert isinstance(image, np.ndarray)


def test_load_image_size():
    image_path = test_path / "data" / "images" / "Sample_0.jpeg"

    image = io.load_image(str(image_path), crop_border=False)

    assert image.shape == (2607, 1834, 3)
