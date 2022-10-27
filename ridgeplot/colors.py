"""This module collects functions for manipulating color legends
for matplotlib plots and a collections of color palettes. 
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any

import matplotlib.axes
import matplotlib.patches as mpatches
from matplotlib import legend

ColorPalette: dict[str, list[str]] = dict(
    # 1. maximum
    # modified from:
    # https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
    maximum=[
        "#f58231",
        "#e6194b",
        "#3cb44b",
        "#ffe119",
        "#4363d8",
        "#911eb4",
        "#03A8FB",
        "#F8BF6C",
        "#CAF5CB",
        "#fabebe",
        "#008080",
        "#e6beff",
        "#9a6324",
        "#fffac8",
        "#800000",
        "#aaffc3",
        "#808000",
        "#ffd8b1",
        "#000075",
        "#808080",
        "#ffffff",
        "#000000",
    ],
    # 2. simpsons
    # A palette from ggsci R package
    # https://github.com/road2stat/ggsci/blob/master/data-raw/data-generator.R
    simpsons=[
        "#FED439",
        "#709AE1",
        "#8A9197",
        "#D2AF81",
        "#FD7446",
        "#D5E4A2",
        "#197EC0",
        "#F05C3B",
        "#46732E",
        "#71D0F5",
        "#370335",
        "#075149",
        "#C80813",
        "#91331F",
        "#1A9993",
        "#FD8CC1",
    ],
    # 3. okabeito:
    # Color palette proposed by Okabe and Ito
    # copy from colorboindr R package
    # https://github.com/clauswilke/colorblindr/blob/master/R/palettes.R
    okabeito=[
        "#E69F00",
        "#56B4E9",
        "#009E73",
        "#F0E442",
        "#0072B2",
        "#D55E00",
        "#CC79A7",
        "#999999",
    ],
    # 4. invitae:
    # https://www.buyayo.com/invitae
    invitae=[
        "#A3CF71",
        "#66BF7E",
        "#0AACA0",
        "#0888B2",
        "#373737",
        "#EFEDEA",
        "#686b69",
        "#417d55",
    ],
)


def ordered_set(xs: list[str]) -> list[str]:
    """
    this is a simple function to make a set according to the order of the input list

    because python set is unordered, https://stackoverflow.com/questions/9792664/converting-a-list-to-a-set-changes-element-order

    Args:
        xs: list of input values

    Returns:
        a list of unique input values in the order of how they arranged in the input list
    """
    xs = list(xs)
    return sorted(set(xs), key=xs.index)


def check_color_vector_size(categorical_vector: list[str], color_vector: list[str]) -> list[str]:
    """
    asserting the number of different categories in the input list is less than the given color list

    Args:
        categorical_vector: list of input values (i.e. labels of the samples), can be duplicated
        color_vector: list of colors, intentionally not checked for duplication

    Returns:
        list of unique categories in the input list
    """
    categories = ordered_set(categorical_vector)

    if len(categories) > len(color_vector):
        raise ValueError(f"Not enough colors!! {len(color_vector)} colors for {len(categories)} categories")
    return categories


class ColorEncoder:
    """
    color-encoding a categoric vector

    Example:
        ```
        >>> categorical_vector = ['group a','group b','group c','group a']
        >>> colors = ColorPalette["okabeito"]
        >>> ce = ColorEncoder()
        >>> ce.fit(categorical_vector, colors)
        >>> ce.encoder
        OrderedDict([('group a', '#E69F00'),
             ('group b', '#56B4E9'),
             ('group c', '#009E73')])
        >>> ce.transform(["group b", "group c", "group a"])
        ['#56B4E9', '#009E73', '#E69F00']
        ```

    or:
        ```
        >>> ce = ColorEncoder()
        >>> ce.fit_transform(categorical_vector, colors)
        ['#E69F00', '#56B4E9', '#009E73', '#E69F00']
        ```

    access color encoder:
        ```
        >>> ce.encoder
        OrderedDict([('group a', '#E69F00'),
             ('group b', '#56B4E9'),
             ('group c', '#009E73')])
        ```
    """

    def __init__(self):
        self.x: list[str] = list()
        self.distinct_categories: list[str] = []
        self.encoder: OrderedDict[str, str] = OrderedDict()

    def fit(self, categories: list[str], colors: list[str] = ColorPalette["invitae"]) -> None:
        """
        mapping colors to the unique categories in the input list
        basically fill the encoder dictionary

        Example:
            ```
            >>> categorical_vector = ['group a','group b','group c','group a']
            >>> colors = ColorPalette["okabeito"]
            >>> ce = ColorEncoder()
            >>> ce.fit(categroical_vector, colors)
            ```

        Args:
            categories: list of input values (i.e. labels of the samples), can be duplicated
            colors: list of colors, intentionally not checked for duplication
        Returns:
            NoneType
        """
        self.distinct_categories = check_color_vector_size(categories, colors)
        self.encoder = OrderedDict({category: col for category, col in zip(self.distinct_categories, colors)})

    def transform(self, categories: list[str]) -> list[str]:
        """
        mapping color to the a list of category in the input list

        Example:
            ```
            >>> categorical_vector = ['group a','group b','group c','group a']
            >>> colors = ColorPalette["okabeito"]
            >>> ce = color_encoder()
            >>> ce.fit(categroical_vector, colors)
            >>> new_categorical_vector = ["group b", "group c"]
            >>> ce.transform(new_categorical_vector)
            ['#56B4E9', '#009E73']
            ```

        Args:
            categories: list of input values (i.e. labels of the samples), can be duplicated
        Returns:
            list of colors for the input list according to the fitted color encoder
        """
        if not self.encoder:
            raise ValueError("Call color_encoder.fit() first!!")

        union_set = set(self.distinct_categories).union(set(categories))
        if len(union_set) != len(self.distinct_categories):
            unseen = union_set - set(self.distinct_categories)
            unseen_str = ", ".join(sorted(list(unseen)))
            raise ValueError(f"Input [categories] contain unseen data!!: {unseen_str}")

        return [self.encoder[category] for category in categories]

    def fit_transform(self, categories: list[str], colors: list[str] = ColorPalette["invitae"]) -> list[str]:
        """
        first map the color to the categories, and then return the corresponding color for each category in the input list

        Example:
            ```
            >>> categorical_vector = ["group1", "group2", "group1"]
            >>> colors = ["salmon","gold"]
            >>> ce = ColorEncoder()
            >>> ce.fit_transform(categorical_vector, colors)
            ['salmon', 'gold', 'salmon']
            ```

        Args:
            categories: list of input values (i.e. labels of the samples), can be duplicated
            colors: list of colors to be assigned to the categories
        Returns:
            list of colors corresponding to the input
        """
        self.fit(categories, colors=colors)
        return self.transform(categories)

    def show_legend(self, ax: matplotlib.axes, sort: bool = False, **kwargs: dict[str, Any]) -> legend.Legend:
        """
        Adding matplotlib legend describing the color encoder to a matplotlib ax object

        Args:
            ax: matplotlib ax object
            sort: sort the legend by the category
            **kwargs: keyword arguments for matplotlib.pyplot.legend

        Returns:
            the matplotlib legend object
        """

        if sort:
            self.encoder = OrderedDict(sorted(self.encoder.items(), key=lambda item: item[0]))
        pat = [mpatches.Patch(color=col, label=lab) for lab, col in self.encoder.items()]
        lgd = ax.legend(handles=pat, **kwargs)
        return lgd
