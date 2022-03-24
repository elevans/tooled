import pandas as pd
from matplotlib import pyplot as plt
from typing import List


def plot_3d(axes: List[str], data: pd.DataFrame, show=True):
    """Plot 3D data.

    Plot 3D data

    :param data: 3D data in a pandas DataFrame.
    :param axes:
        List of axes labels in the input DataFrame (i.e. column names). If no axes
        are provided, the first 3 columns of the input DataFrame will automatically be used.
    :param show: Set to display graph.
    """

    if axes == None:
        axes = data.columns.tolist()

    fig = plt.figure()
    ax = fig.add_subplot(111 ,projection='3d')
    x = data[axes[0]]
    y = data[axes[1]]
    z = data[axes[2]]
    ax.scatter(x, y, z)
    ax.set_xlabel(axes[0])
    ax.set_ylabel(axes[1])
    ax.set_zlabel(axes[2])

    if show:
        plt.show()