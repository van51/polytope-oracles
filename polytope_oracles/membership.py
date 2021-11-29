from typing import Optional, Any, List

import numpy as np
from dingo import HPolytope as Polytope
from polytope_oracles.utils import project
from n2 import HnswIndex


class Membership:
    def __init__(self, *, A: np.array = Optional[None], b: Optional[np.array] = None,
                 polytope: Optional[Polytope] = None, internal_point: Optional[np.array] = None) -> None:
        """
        Construct a membership oracle for a polytope. You can define the polytope in two ways:
            - provide its H-representation `A x <= b` (where A is an `n x d` matrix
                and b is an `n x 1` matrix). In this case the represenation is assumed
                to be full-dim and minimum.
            - provide an already constructed Polytope objects.
        :param A:
        :param b:
        :param polytope:
        :param internal_point:
        """
        if polytope is None:
            if A is None or b is None:
                raise ValueError("Specify one of (A, b) or polytope")
            self.polytope = Polytope(A, b)
        else:
            self.polytope = polytope

        # TODO compute chebyshev center if not provided
        self._internal_point = np.zeros(self.polytope.dimension()) if internal_point is None else internal_point
        self._external_points: List[np.array] = self.compute_external_points()
        self._index: Any = None
        self._index_type: str = ""

    def initialize(self, index_type: str = "n2", **kwargs) -> None:
        """

        :param index_type: Accepted values: "annoy", "hnswlib", "n2". Default is "n2"
        :param kwargs: Parameters for the respective index types. Please check the corresponding create_*_nn function.
        :return:
        """
        if index_type == "n2":
            self.create_n2_nn(**kwargs)
        elif index_type == "hnswlib":
            self.create_hnsw_nn(**kwargs)
        elif index_type == "annoy":
            self.create_annoy_nn(**kwargs)

    def create_annoy_nn(self, n_trees: int = 10) -> None:
        from annoy import AnnoyIndex

        self._index_type = "annoy"
        self._index = AnnoyIndex(self.polytope.dimension(), "euclidean")
        for i, point in enumerate(self._external_points + [self._internal_point]):
            self._index.add_item(i, point)

        self._index.build(n_trees)
    
    def create_n2_nn(self, m: int = 15, max_m0: Optional[int] = None, ef_construction=None, n_threads=None, mult=None, neighbor_selecting=None, graph_merging=None):
        self._index_type = "n2"
        self._index = HnswIndex(self.polytope.dimension(), 'L2')
        for point in self._external_points + [self._internal_point]:
            self._index.add_data(point)
        self._index.build(m=m, max_m0=max_m0, ef_construction=ef_construction, n_threads=n_threads, mult=mult, neighbor_selecting=neighbor_selecting, graph_merging=graph_merging)

    def create_hnsw_nn(self, m: int = 15):
        import hnswlib

        self._index_type = "hnswlib"
        self._index = hnswlib.Index(space = 'l2', dim = self.polytope.dimension())
        self._index.init_index(max_elements=len(self._external_points)+1, ef_construction = 200, M = m)
        self._index.add_items(self._external_points + [self._internal_point], range(len(self._external_points)+1))

    def compute_external_points(self) -> List[np.array]:
        external_points: List[np.array] = []
        for a, b in zip(self.polytope.A(), self.polytope.b()):
            projected_point = project(self._internal_point, a, b)
            external_points.append(2 * projected_point - self._internal_point)
        return external_points

    def contains(self, point: np.array) -> bool:
        assert self._index is not None, 'You should initialize the data structure first'

        if self._index_type == "n2":
            ann = self._index.search_by_vector(point, k=1)[0]
        elif self._index_type == "annoy":
            ann = self._index.get_nns_by_vector(point, 1, search_k=-1, include_distances=False)[0]
        elif self._index_type == "hnswlib":
            ann = self._index.knn_query(point, k=1)[0]

        return ann == len(self._external_points)
