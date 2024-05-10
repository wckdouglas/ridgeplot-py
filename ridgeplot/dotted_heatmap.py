"""
for most of the part, this is copied from:
https://stackoverflow.com/questions/59381273/heatmap-with-circles-indicating-size-of-population
"""

from __future__ import annotations

from typing import Optional

import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import PatchCollection


def dotted_heatmap(
    data: pd.DataFrame,
    ax: matplotlib.axes._axes.Axes,
    cmap: str = "cividis",
    circle_size: Optional[float] = None,
):
    """
    Plotting dotted heatmap

    Example:
        ```
        >>> import matplotlib.pyplot as plt
        >>> from ridgeplot.dotted_heatmap import dotted_heatmap
        >>> fig = plt.figure()
        >>> ax = fig.add_subplot(111)
        >>> data = pd.DataFrame(
        ...    np.random.randn(n, n),
        ...    index=[f"feature{i}" for i in range(n)],
        ...    columns=[f"sample{i}" for i in range(n)],
        ... )
        >>> dotted_heatmap(data=data,ax=ax, cmap="viridis")
        ```

    Args:
        data: data to plot
        ax: matplotlib ax object
        cmap: cmap value, defaults to "cividis"
        circle_size: raidus of the circles,
            if None, we will use relaive sizes, defaults to None
    """
    nrows, ncols = data.shape
    x, y = np.meshgrid(np.arange(ncols), np.arange(nrows))
    radii = data.values / 2 / data.values.max()
    # radius is relative if circle_size is None
    circles = [
        plt.Circle((j, i), radius=circle_size if circle_size is not None else r)
        for r, j, i in zip(radii.flat, x.flat, y.flat)
    ]
    col = PatchCollection(circles, array=data.values.flatten(), cmap=cmap)
    ax.add_collection(col)

    ax.set_xticks(np.arange(ncols))
    ax.set_xticklabels(data.columns)
    ax.set_yticks(np.arange(nrows))
    ax.set_yticklabels(data.index)

    ax.set_xticks(np.arange(ncols + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(nrows + 1) - 0.5, minor=True)
    ax.grid(which="minor", alpha=0.5, color="white")
    ax.tick_params(left=False, bottom=False)
    for d in ["top", "bottom", "left", "right"]:
        ax.spines[d].set(alpha=0.5)
    plt.colorbar(col)
