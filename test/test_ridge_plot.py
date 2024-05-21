import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytest
from ridgeplot import RidgePlotError, ridgeplot

matplotlib.use("agg")


@pytest.fixture(scope="module")
def data():
    data_dict = {}
    for i in range(10):
        data_dict["data_{}".format(i)] = np.random.randn(100) * (i + 1)
    return data_dict


def test_ridgeplot_bad_fill_color(data):
    figure = plt.figure()
    ax = figure.add_subplot(111)
    with pytest.raises(RidgePlotError) as e:
        ridgeplot(ax=ax, data=data, fill_colors=["white", "white"])
    assert "fill_colors must be same length as data" in str(e.value), "Failed to catch fill color length diff"


def test_ridgeplot_bad_line_color(data):
    figure = plt.figure()
    ax = figure.add_subplot(111)
    with pytest.raises(RidgePlotError) as e:
        ridgeplot(ax=ax, data=data, line_colors=["white", "white"])
    assert "line_colors must be same length as data" in str(e.value), "Failed to catch line color length diff"


def test_ridgeplot(data):
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ridgeplot(ax, data, xlim=(-20, 20))
