import numpy as np


def project(p: np.array, a: np.array, b: np.array) -> np.array:
    """
    Project point p on hyperplane defined by a and b
    :param point:
    :param a:
    :param b:
    :return: the projected point
    """
    return p - a * ((p.dot(a) - b) / a.dot(a))
