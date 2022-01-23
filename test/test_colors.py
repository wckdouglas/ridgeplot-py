from unittest.mock import patch

import pytest

from ridgeplot.colors import (
    ColorEncoder,
    ColorPalette,
    check_color_vector_size,
    ordered_set,
)


@pytest.fixture(scope="module")
def color_encoder():
    ce = ColorEncoder()
    ce.fit(["a", "b", "c", "b", "a"], ["red", "green", "blue"])
    return ce


@pytest.mark.parametrize(
    "input, output",
    [(["a", "b", "c"], ["a", "b", "c"]), (["b", "a", "b", "d"], ["b", "a", "d"])],
)
def test_ordered_set(input, output):
    assert ordered_set(input) == output


@pytest.mark.parametrize(
    "palette, expected_num",
    [("maximum", 22), ("simpsons", 16), ("okabeito", 8)],
)
def test_ColorPalette(palette, expected_num):
    assert len(ColorPalette[palette].value) == expected_num


def test_check_color_vector_size():
    cat = check_color_vector_size(["a", "a", "b", "a"], ["red", "blue"])
    assert set(cat).union(set(["a", "b"])) == set(["a", "b"])


def test_check_color_vector_size_fail():
    with pytest.raises(ValueError) as e:
        check_color_vector_size(["a", "a", "b", "c"], ["red", "blue"])
    assert "Not enough colors!!" in str(e.value), "Cannot catch category > color"


def test_ColorEncoder(color_encoder):
    assert color_encoder.encoder == {"a": "red", "b": "green", "c": "blue"}


def test_ColorEncoder_transform(color_encoder):
    assert color_encoder.transform(["c", "c", "c"]) == ["blue", "blue", "blue"]


def test_ColorEncoder_transform_unseen(color_encoder):
    with pytest.raises(ValueError) as e:
        color_encoder.transform(["a", "b", "c", "d", "e"])
    assert "Input [categories] contain unseen data!!: d, e" in str(e.value)


def test_ColorEncoder_transform_fail():
    with pytest.raises(ValueError) as e:
        ce = ColorEncoder()
        ce.transform(["a", "b", "c"])
    assert "Call color_encoder.fit() first" in str(e.value)


def test_ColorEncoder_fit_transform(color_encoder):
    colors = color_encoder.fit_transform(
        ["a", "b", "c", "b", "a"], ["red", "green", "blue"]
    )
    assert color_encoder.encoder == {"a": "red", "b": "green", "c": "blue"}
    assert colors == ["red", "green", "blue", "green", "red"]


@patch("matplotlib.pyplot.figure")
def test_ColorEncoder_show_legend(figure, color_encoder):
    ax = figure.add_subplot(111)
    color_encoder.show_legend(ax)


@patch("matplotlib.pyplot.figure")
def test_ColorEncoder_show_legend_sort(figure, color_encoder):
    ax = figure.add_subplot(111)
    color_encoder.show_legend(ax, sort=True)
