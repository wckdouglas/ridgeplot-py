import numpy as np
import pytest

from ridgeplot.stats import scaling


@pytest.mark.parametrize("xs,expected", [([1, 2, 3, 4], [0, 0.333, 0.666, 1]), ([8, 6, 4, 2], [1, 0.666, 0.333, 0])])
def test_scaling(xs, expected):
    out = scaling(xs)
    assert np.all(np.isclose(out, expected, atol=0.001)), "Failed test"
