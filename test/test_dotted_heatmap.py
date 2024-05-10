from unittest.mock import patch

import numpy as np
import pandas as pd

from ridgeplot import dotted_heatmap


@patch("matplotlib.pyplot.figure")
def test_ridgeplot(figure):
    ax = figure.add_subplot(111)
    n = 10
    data = pd.DataFrame(
        np.random.randn(n, n),
        index=[f"feature{i}" for i in range(n)],
        columns=[f"sample{i}" for i in range(n)],
    )
    dotted_heatmap.dotted_heatmap(data=data, ax=ax, cmap="viridis", circle_size=None)
