import numpy as np
from dingo import HPolytope as Polytope


class SphereBasedSampler:

    def __init__(self, mu: float = 0.0, sigma: float = 1.0, seed: int = 42):
        self.generator = np.random.default_rng(seed)
        self.mu = mu
        self.sigma = sigma
        self.seed = seed

    def generate(self, n: int, d: int) -> Polytope:
        """
        :param n: Number of facets
        :param d: The target dimension
        :return: a generated polytope
        """

        points = self.generator.normal(self.mu, self.sigma, (n, d))
        norms = np.linalg.norm(points, axis=1, keepdims=True)
        points = points / norms

        return Polytope(np.array(points), np.ones(n))
