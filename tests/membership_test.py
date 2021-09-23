from polytope_oracles.membership import Membership
from polytope import box2poly, Polytope
import pytest


def test_internal_point():
    polytope: Polytope = box2poly([[-1, 1], [-1, 1]])
    membership = Membership(polytope=polytope)
    assert (membership._internal_point == [0, 0]).all()

    polytope: Polytope = box2poly([[-1, 1], [-1, 1], [0, 2]])
    membership = Membership(polytope=polytope)
    assert (membership._internal_point == [0, 0, 1]).all()


def test_external_points():
    polytope: Polytope = box2poly([[-1, 1], [-1, 1]])
    membership = Membership(polytope=polytope)
    expected_external_points = {(0, 2), (0, -2), (2, 0), (-2, 0)}
    assert len(membership._external_points) == len(expected_external_points)
    assert set([tuple(p.tolist()) for p in membership._external_points]) == expected_external_points


def test_annoy_index():
    polytope: Polytope = box2poly([[-1, 1], [-1, 1]])
    membership = Membership(polytope=polytope)

    query = [0.5, 0.5]
    with pytest.raises(AssertionError):
        membership.contains(query)

    membership.create_annoy_nn(2)
    assert membership.contains(query)

    assert not membership.contains([2, 0])
