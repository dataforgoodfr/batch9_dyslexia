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


def plot_2_images(img1: np.ndarray, img2: np.ndarray, figsize=(18, 9)):
    """Plots original image and the processed one

    Parameters
    ----------
    img1 : np.ndarray
        Original image
    img2 : np.ndarray
        Preprocessed image
    figsize : tuple, default (18, 9)
        Figure size
    """

    fig, axes = plt.subplots(1, 2, figsize=figsize)

    ax = axes[0]
    ax.imshow(img1)
    ax.set_title('Original')

    ax = axes[1]
    ax.imshow(img2, cmap='gray')
    ax.set_title('Preprocessed')

    plt.show()