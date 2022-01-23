from collections import OrderedDict
from enum import Enum
from typing import List

import matplotlib.axes as mpl_axes  # type: ignore
import matplotlib.patches as mpatches  # type: ignore
from matplotlib import legend  # type: ignore


class ColorPalette(Enum):
    """
    Enum for the different color palettes

    1. maximum
    modified from:
    https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/

    2. simpsons
    A palette from ggsci R package
    https://github.com/road2stat/ggsci/blob/master/data-raw/data-generator.R

    3. okabeito:
    Color palette proposed by Okabe and Ito
    copy from colorboindr R package
    https://github.com/clauswilke/colorblindr/blob/master/R/palettes.R
    """

    maximum: List[str] = [
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
    ]
    simpsons: List[str] = [
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
    ]
    okabeito: List[str] = [
        "#E69F00",
        "#56B4E9",
        "#009E73",
        "#F0E442",
        "#0072B2",
        "#D55E00",
        "#CC79A7",
        "#999999",
    ]


def ordered_set(xs: List[str]) -> List[str]:
    """
    this is a simple function to make a set according to the order of the input list

    because python set is unordered, https://stackoverflow.com/questions/9792664/converting-a-list-to-a-set-changes-element-order

    :param List[str] xs: list of input values
    :return:  a list of unique input values in the order of how they arranged in the input list
    :rtype: List[str]
    """
    xs = list(xs)
    return sorted(set(xs), key=xs.index)


def check_color_vector_size(categorical_vector: List[str], color_vector: List[str]) -> List[str]:
    """
    asserting the number of different categories in the input list is less than the given color list

    :param List[str] categorical_vector: list of input values (i.e. labels of the samples), can be duplicated
    :param List[str] color_vector: list of colors, intentionally not checked for duplication
    :return: list of unique categories in the input list
    :rtype: List[str]
    """
    categories = ordered_set(categorical_vector)

    if len(categories) > len(color_vector):
        raise ValueError(f"Not enough colors!! {len(color_vector)} colors for {len(categories)} categories")
    return categories


class ColorEncoder:
    """
    color-encoding a categoric vector
    Example::
        categorical_vector = ['a','b','c','a']
        colors = obakeito_palette()
        ce = color_encoder()
        ce.fit(categorical_vector, colors)
        encoded_colors = ce.transform(new_categorical_vector)
    or::
        ce = color_encoder()
        encoded_colors = ce.fit_transform(categorical_vector, colors)
    access color encoder::
        encoded_color_map = ce.encoder
    """

    def __init__(self):
        self.x: List[str] = list()
        self.distinct_categories: List[str] = list()
        self.encoder: OrderedDict[str, str] = list()

    def fit(self, categories: List[str], colors: List[str] = ColorPalette.okabeito.value) -> None:
        """
        mapping colors to the unique categories in the input list
        basically fill the encoder dictionary

        Example::
            ce = color_encoder()
            ce.fit(categroical_vector, colors)

        :param List[str] categories: list of input values (i.e. labels of the samples), can be duplicated
        :param List[str] colors: list of colors, intentionally not checked for duplication
        :return: None
        :rtype: NoneType
        """
        self.distinct_categories = check_color_vector_size(categories, colors)
        self.encoder = OrderedDict({category: col for category, col in zip(self.distinct_categories, colors)})

    def transform(self, categories: List[str]) -> List[str]:
        """
        mapping color to the a list of category in the input list

        Example::
            ce = color_encoder()
            ce.fit(categroical_vector, colors)
            encoded_colors = ce.transform(new_categorical_vector)

        :parma List[str] categories: list of input values (i.e. labels of the samples), can be duplicated
        :return: list of colors for the input list according to the fitted color encoder
        :rtype: List[str]

        """
        if not self.encoder:
            raise ValueError("Call color_encoder.fit() first!!")

        union_set = set(self.distinct_categories).union(set(categories))
        if len(union_set) != len(self.distinct_categories):
            unseen = union_set - set(self.distinct_categories)
            unseen_str = ", ".join(sorted(list(unseen)))
            raise ValueError(f"Input [categories] contain unseen data!!: {unseen_str}")

        return [self.encoder[category] for category in categories]

    def fit_transform(self, categories: List[str], colors: List[str] = ColorPalette.okabeito.value) -> List[str]:
        """
        first map the color to the categories, and then return the corresponding color for each category in the input list

        Example::
            ce = color_encoder()
            encoded_colors = ce.fit_transform(categorical_vector, colors)

        :param List[str] xs: list of input values (i.e. labels of the samples), can be duplicated
        """
        self.fit(categories, colors=colors)
        return self.transform(categories)

    def show_legend(self, ax: mpl_axes, sort: bool = False, **kwargs) -> legend.Legend:
        """
        Adding matplotlib legend describing the color encoder to a matplotlib ax object

        :param matplotlib.axes._axes.Axe ax: matplotlib ax object
        :param bool sort: sort the legend by the category
        :param kwargs: keyword arguments for matplotlib.pyplot.legend
        :return: the matplotlib legend object
        :rtype: matplotlib.legend.Legend
        """

        if sort:
            self.encoder = OrderedDict(sorted(self.encoder.items(), key=lambda item: item[0]))
        pat = [mpatches.Patch(color=col, label=lab) for lab, col in self.encoder.items()]
        lgd = ax.legend(handles=pat, **kwargs)
        return lgd
