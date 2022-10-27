import numpy as np
import numpy.typing as npt


def scaling(x: list[float]) -> npt.NDArray[np.float64]:
    """
    scaling a vector to a range between 0 and 1

    Example:
        ```
        >>> scaling([1,2,3,4])
        array([0.        , 0.33333333, 0.66666667, 1.        ])
        ```

    Args:
        x: list of data values (float)

    Returns:
        An numpy array of the scaled values
    """
    np_x = np.array(x, dtype="float")

    if len(np.unique(np_x)) == 1:
        raise ValueError("The input list should not be homogenous")

    np_x = (np_x - np_x.min()) / (np_x.max() - np_x.min())
    return np_x
