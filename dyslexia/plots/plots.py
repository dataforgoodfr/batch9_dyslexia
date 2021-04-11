import matplotlib.pyplot as plt
import numpy as np


def plot_image(img: np.ndarray, figsize=(10, 10), gray=True):
    """Plot one image

    Parameters
    ----------
    img : np.ndarray
        Source image
    figsize : tuple, default (10, 10)
        Figure size
    gray : bool, default True
        Whether it's a grayscale image or not
    """

    fig = plt.figure(figsize=figsize)

    if gray:
        plt.imshow(img, cmap='gray')
    else:
        plt.imshow(img)

    plt.show()


def plot_2_images(img1: np.ndarray, img2: np.ndarray, figsize=(18, 9), gray=(False, True)):
    """Plots original image and the processed one

    Parameters
    ----------
    img1 : np.ndarray
        Original image
    img2 : np.ndarray
        Preprocessed image
    figsize : tuple, default (18, 9)
        Figure size
    gray: tuple(bool), default (False, True)
        Whether it's a grayscale image or not
    """

    fig, axes = plt.subplots(1, 2, figsize=figsize)

    ax = axes[0]
    if gray[0]:
        ax.imshow(img1, cmap='gray')
    else:
        ax.imshow(img1)

    ax = axes[1]
    if gray[1]:
        ax.imshow(img2, cmap='gray')
    else:
        ax.imshow(img2)

    plt.show()