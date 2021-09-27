import xarray as xr
from math import sqrt
from skimage.feature import blob_log
from skimage.color import rgb2gray
from matplotlib import pyplot as plt

def find_blobs(image, min_sigma, max_sigma, num_sigma, threshold=0.1, show=False) -> list:
    """
    Find blobs in a given image.
    :param image: Input image (numpy or xarray).
    :param min_sigma: Keep small to detect smaller blobs (recommended: 0.47).
    :param max_sigma: Keep large to detect larger blobs (recommended: 2).
    :param num_sigma: Number of intermediate values of standard deviation between min and max sigma (recommended: 50).
    :param threshold: Threshold value (recommended: 0.008).
    :param show: Display identified blobs over input image.
    :return: List of detected blobs.
    """
    if isinstance(image, xr.DataArray):
        image = image.squeeze()
        image = image.data

    # detect blobs
    image_gray_scale = rgb2gray(image)
    blobs = blob_log(image_gray_scale, min_sigma=min_sigma, max_sigma=max_sigma, num_sigma=num_sigma, threshold=threshold)
    blobs[:, 2] = blobs[:, 2] * sqrt(2)

    if show:
        fig, ax = plt.subplots(figsize=(10,8), sharex=True, sharey=True)
        ax.imshow(image, interpolation='nearest')
        for blob in blobs:
            y, x, r = blob
            c = plt.Circle((x, y), r, color='blue', linewidth=2, fill=False)
            ax.add_patch(c)

        plt.tight_layout()
        plt.show()

    return blobs