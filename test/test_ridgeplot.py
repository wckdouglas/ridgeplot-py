from unittest.mock import patch

import numpy as np
import pytest

from ridgeplot import ridgeplot, RidgePlotError


@pytest.fixture(scope='module')
def data():
    data_dict = {}
    for i in range(10):
        data_dict['data_{}'.format(i)] = np.random.randn(100) * (i+1)
    return data_dict



@patch('matplotlib.pyplot.figure')
def test_ridgeplot_bad_fill_color(figure, data):
    ax = figure.add_subplot(111)
    with pytest.raises(RidgePlotError) as e:
        ridgeplot(ax=ax, data=data, fill_colors=['white','white'])
    assert 'fill_colors must be same length as data' in str(e.value), "Failed to catch fill color length diff"


@patch('matplotlib.pyplot.figure')
def test_ridgeplot_bad_line_color(figure, data):
    ax = figure.add_subplot(111)
    with pytest.raises(RidgePlotError) as e:
        ridgeplot(ax=ax, data=data, line_colors=['white','white'])
    assert 'line_colors must be same length as data' in str(e.value), "Failed to catch line color length diff"



@patch("matplotlib.pyplot.figure")
def test_ridgeplot(figure, data):
    ax = figure.add_subplot(111)
    ridgeplot(ax, data, xlim=(-20,20))