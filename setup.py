
from setuptools import setup
from setuptools import find_packages
import os

path = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(path, "requirements.txt"), encoding="utf-8") as f:
        REQUIRED = f.read().split("\n")
except:
    REQUIRED = []

setup(
    name="dyslexia",
    version="0.1",
    description="Python package for Dyslex'IA company. Contains OCR utils.",
    author="Dyslex'IA",
    url="https://github.com/dataforgoodfr/batch9_dyslexia",
    install_requires=REQUIRED,
    package_data={'dyslexia': ['src/blur_detection_model.sav']},
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={"console_scripts": ["dyslexia=dyslexia.eval.main:cli"]},
    packages=find_packages(exclude=("example", "app", "data", "docker", "tests")),
)