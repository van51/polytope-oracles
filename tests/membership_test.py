from polytope_oracles.membership import Membership
from polytope import box2poly
from volestipy import HPolytope as Polytope
import pytest


def test_internal_point():
    polytope_ = box2poly([[-1, 1], [-1, 1]])
    polytope = Polytope(polytope_.A, polytope_.b)
    membership = Membership(polytope=polytope)
    assert (membership._internal_point == [0, 0]).all()

    polytope_ = box2poly([[-1, 1], [-1, 1], [0, 2]])
    polytope = Polytope(polytope_.A, polytope_.b)
    membership = Membership(polytope=polytope)
    assert (membership._internal_point == [0, 0, 0]).all()


def test_external_points():
    polytope_ = box2poly([[-1, 1], [-1, 1]])
    polytope = Polytope(polytope_.A, polytope_.b)
    membership = Membership(polytope=polytope)
    expected_external_points = {(0, 2), (0, -2), (2, 0), (-2, 0)}
    assert len(membership._external_points) == len(expected_external_points)
    assert set([tuple(p.tolist()) for p in membership._external_points]) == expected_external_points


@pytest.mark.parametrize('index_type', ["n2", "hnswlib", "annoy"])
def test_index(index_type):
    polytope_ = box2poly([[-1, 1], [-1, 1]])
    polytope = Polytope(polytope_.A, polytope_.b)
    membership = Membership(polytope=polytope)

    query = [0.5, 0.5]
    with pytest.raises(AssertionError):
        membership.contains(query)

    membership.initialize(index_type)
    assert membership.contains(query)

    assert not membership.contains([2, 0])
