# ridgeplot-py #

[![CI](https://github.com/wckdouglas/ridgeplot-py/actions/workflows/ci.yaml/badge.svg)](https://github.com/wckdouglas/ridgeplot-py/actions/workflows/ci.yaml) [![codecov](https://codecov.io/gh/wckdouglas/ridgeplot-py/branch/main/graph/badge.svg?token=2owCGZa1K4)](https://codecov.io/gh/wckdouglas/ridgeplot-py)


A simple module for plotting [ridgeplot](https://clauswilke.com/blog/2017/09/15/goodbye-joyplots/) with the [scipy ecosystem](https://www.scipy.org/about.html).

## Install ##

```bash
git clone git@github.com:wckdouglas/ridgeplot-py.git
cd ridgeplot-py
python setup.py install 
```

## Usage ##

```python
from ridgeplot import ridgeplot
from ridgeplot.colors import ColorEncoder, ColorPalette
import numpy as np
import matplotlib.pyplot as plt

# mocking some data
# the input data should be a dict of
# - keys: group names for the distributions
# - values: list of values 
data = {}
for i in range(8):
    data['data_{}'.format(i)] = np.random.randn(100) * (i+1)

# make the plot
fig = plt.figure()
ax = fig.add_subplot(111)
ridgeplot(
    ax, 
    data, 
    xlim=(-20,20), 
    label_size=15
)
```


## Example ##

A [notebook](https://github.com/wckdouglas/ridgeplot-py/blob/main/Example.ipynb) showing quick howto is included in this repo!