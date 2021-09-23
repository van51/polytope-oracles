from polytope_oracles.utils import project
import numpy as np


def test_project():
    p = np.array([0, 0])
    A = np.array([1, 0])
    b = np.array([1])
    assert (project(p, A, b) == np.array([1, 0])).all()

    A = np.array([1, 1])
    assert (project(p, A, b) == np.array([0.5, 0.5])).all()

    p = np.array([0, 0, 0])
    A = np.array([1, 0, 0])
    b = np.array([1])
    assert (project(p, A, b) == np.array([1, 0, 0])).all()

    A = np.array([0, 1, 0])
    assert (project(p, A, b) == np.array([0, 1, 0])).all()
