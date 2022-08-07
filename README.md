# ridgeplot-py #

[![CI](https://github.com/wckdouglas/ridgeplot-py/actions/workflows/ci.yaml/badge.svg)](https://github.com/wckdouglas/ridgeplot-py/actions/workflows/ci.yaml) [![codecov](https://codecov.io/gh/wckdouglas/ridgeplot-py/branch/main/graph/badge.svg?token=2owCGZa1K4)](https://codecov.io/gh/wckdouglas/ridgeplot-py)


This is a simple module for plotting [ridgeplot](https://clauswilke.com/blog/2017/09/15/goodbye-joyplots/) with the [scipy ecosystem](https://www.scipy.org/about.html).

Ridgeplot is a great data visualization technique to compare distributions from multiple groups at the same time, and was first introduced in 2017 as joy plot:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">I hereby propose that we call these &quot;joy plots&quot; <a href="https://twitter.com/hashtag/rstats?src=hash&amp;ref_src=twsrc%5Etfw">#rstats</a> <a href="https://t.co/uuLGpQLAwY">https://t.co/uuLGpQLAwY</a></p>&mdash; Jenny Bryan (@JennyBryan) <a href="https://twitter.com/JennyBryan/status/856674638981550080?ref_src=twsrc%5Etfw">April 25, 2017</a></blockquote> 

[ridgeplot-py](https://pypi.org/project/ridgeplot-py/) provides a simple API to produce matplotlib-compatible ridgeplots, as well as a handy [ColorEncoder](https://github.com/wckdouglas/ridgeplot-py/blob/0198628ce0622e2e7f4f4e9284165d5d09324ca9/ridgeplot/colors.py#L117) class with scikit-learn syntax for manipulating color annotations in a consistent way [through out manuscripts or presentations].

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

![img](https://raw.githubusercontent.com/wckdouglas/ridgeplot-py/main/img/ridgeplot.png)


## Example ##

A [notebook](https://github.com/wckdouglas/ridgeplot-py/blob/main/Example.ipynb) showing quick howto is included in this repo!