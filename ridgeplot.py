from typing import Dict, List, Tuple

import matplotlib.axes._axes
import numpy as np
from more_itertools import first
from scipy.stats import gaussian_kde


class RidgePlotError(Exception):
    pass

def scaling(x: List[float]):
    """
    scaling a vector to a range between 0 and 1

    :param x: list of float data values
    :return: scaled values
    :rtype: np.array
    """
    x = np.array(x, dtype="float")
    x = (x - x.min()) / (x.max() - x.min())
    return x


def ridgeplot(
    ax: matplotlib.axes._axes.Axes,
    data: Dict[str, List[float]],
    xlim: Tuple[float, float] = None,
    fill_colors: List[str] = None,
    line_colors: List[str] = None,
    label_size: float = 10.0,
) -> None:
    """
    plotting a ridgeplot

    :param matplotlib.axes._axes.Axes ax: a matplotlib ax object for writing the plot
    :param Dict data: data
    :param Tuple xlim: x-limits for the plot (xmin, xmax)
    :param List[str] fill_colors: colors for the fill under the distribution, must be same length as input data (default: all steelblue)
    :param List[str] line_colors: colors for the line drawing the distribution, must be same length as input data (default: all white)
    :param float label_size: label size of the name of each distribution


    Example::

        import numpy as np
        import matplotlib.pyplot as plt

        data = {}
        for i in range(10):
            data['data_{}'.format(i)] = np.random.randn(100) * (i+1)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ridgeplot(ax, data, xlim=(-20,20))
    """

    # assigning colors if not given
    if fill_colors is None:
        fill_colors = len(data) * ["steelblue"]

    if line_colors is None:
        line_colors = len(data) * ['white']

    #assigning xlims if not given
    if xlim is not None:
        xmin, xmax = xlim
    else:
        xmin = min(first(data.values()))
        xmax = max(first(data.values()))

    # data validation
    if len(fill_colors) != len(data):
        raise RidgePlotError("fill_colors must be same length as data")
    
    if len(line_colors) != len(data):
        raise RidgePlotError("line_colors must be same length as data")


    xlines = []
    for sample_number, (data_key, data_values) in enumerate(data.items()):
        data_values = np.array(data_values, dtype="float")
        xs = np.arange(xmin, xmax * 1.1, 0.01)  # xaxis is 10% wider than data max
        kde = gaussian_kde(data_values)

        baseline = sample_number * 0.7
        ys = scaling(kde.pdf(xs)) + baseline
        ax.plot(xs, ys, color=line_colors[sample_number], lw=2)
        ax.fill(xs, ys, color=fill_colors[sample_number])
        xlines.append(baseline)
        ax.text(xmin, baseline, data_key, ha="right", va="bottom", fontsize=label_size)
    ax.hlines(xlines, xmin=xmin, xmax=xmax * 1.1, color="black", lw=1)
    ax.get_yaxis().set_visible(False)
    for side in ["left", "right", "top"]:
        ax.spines[side].set_visible(False)
    ax.set_xlim(xmin, xmax)
