import numpy as np


class Filter:
    def get_kernel(key: str) -> np.ndarray:
        """Get image convolution kernels.

        Get image convolution kernels as NumPy arrays.

        :param key: Name of the kernel (e.g. "sharp").
        :return: Kernel as a np.array.
        """
        kernels = {
            "emboss": np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]]),
            "sharp": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
            "ridge": np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]),
            "imagej": np.array(
                [
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, 24, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1],
                ]
            ),
            "emboss1": np.array(
                [
                    [0, 0, 0, 0, 0],
                    [0, -2, -1, 0, 0],
                    [0, -1, 1, 1, 0],
                    [0, 0, 1, 2, 0],
                    [0, 0, 0, 0, 0],
                ]
            ),
            "emboss2": np.array(
                [
                    [0, 0, 0, 0, 0],
                    [0, 2, 1, 0, 0],
                    [0, 1, -1, -1, 0],
                    [0, 0, -1, -2, 0],
                    [0, 0, 0, 0, 0],
                ]
            ),
        }

        if key in kernels:
            return kernels[key]
        else:
            raise ValueError(f'Kernel "{key}" not found.')
