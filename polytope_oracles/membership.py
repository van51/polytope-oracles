from typing import Optional, Any, List

import numpy as np
from polytope import Polytope

from polytope_oracles.utils import project


class Membership:
    def __init__(self, *, A: np.array = Optional[None], b: Optional[np.array] = None,
                 polytope: Optional[Polytope] = None) -> None:
        """
        Construct a membership oracle for a polytope. You can define the polytope
        in two ways:
            - provide its H-representation `A x <= b` (where A is an `n x d` matrix
                and b is an `n x 1` matrix). In this case the represenation is assumed
                to be full-dim and minimum.
            - provide an already constructed Polytope objects.
        :param A:
        :param b:
        :param polytope:
        """
        if polytope is None:
            if A is None or b is None:
                raise ValueError("Specify one of (A, b) or polytope")
            self.polytope = Polytope(A, b, minrep=True, fulldim=True)
        else:
            self.polytope = polytope

        self._internal_point: np.array = self.polytope.chebXc
        self._external_points: List[np.array] = self.compute_external_points()
        self._index: Any = None

    def create_annoy_nn(self, n_trees: int = 10) -> None:
        from annoy import AnnoyIndex

        self._index = AnnoyIndex(self.polytope.dim, "euclidean")
        for i, point in enumerate(self._external_points + [self._internal_point]):
            self._index.add_item(i, point)

        self._index.build(n_trees)

    def compute_external_points(self) -> List[np.array]:
        external_points: List[np.array] = []
        for a, b in zip(self.polytope.A, self.polytope.b):
            projected_point = project(self._internal_point, a, b)
            external_points.append(2 * projected_point - self._internal_point)
        return external_points

    def contains(self, point: np.array) -> bool:
        from annoy import AnnoyIndex

        assert isinstance(self._index, AnnoyIndex), "You should create an annoy index first"
        ann = self._index.get_nns_by_vector(point, 1, search_k=-1, include_distances=False)[0]
        return ann == len(self._external_points)
