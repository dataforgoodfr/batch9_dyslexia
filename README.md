# batch9_dyslexia


## OCR devlopment

### Install 

You can install this package by cloning the repository and using this command :

```bash
cd batch9_dyslexia
pip install .
```

You can use `pip install -e .` if you are developing on it.


### `dyslexia` package

| Submodules | Description |
| ---------- | ----------- |
| `io` | Input / Outputs functions such as `load_image()` |
| `plots` | Plots functions such as `plot_image()` |
| `preprocessing` | Preprocessing functions such as `image_to_gray()` |
| `ocr` | OCR functions using tesseract backend |


**Using the package** 

```python
from dyslexia import preprocessing
from dyslexia.io import load_image
from dyslexia.ocr import extract_text_from_image

fpath = 'Exemples/SVT/IMG_20210329_123029.jpg'
image_orig = load_image(fpath)
image_gray = preprocessing.image_to_gray(image_no_shadow, threshold=True)

result = extract_text_from_image(image_gray)
```

### Eval Scripts

```bash
dyslexia eval-txt-folder --truth_path tests/data/truth/ --hypothesis_path tests/data/hypothesis/
```

output
```
wer : 0.16666666666666666
mer : 0.16129032258064516
wil : 0.27311827956989243
wip : 0.7268817204301076
hits : 26.0
substitutions : 4.0
deletions : 0.0
insertions : 1.0
```