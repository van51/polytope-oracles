polytope-oracles
===

Library to assist in answering approximate membership and boundary 
queries on H-polytopes.

## Dependencies


### Dingo

We also depend on [Dingo](https://github.com/GeomScale/dingo) which does not yet have a PyPI package. To install
it do the following (taken from its instructions):

```bash
git clone https://github.com/GeomScale/dingo.git
cd dingo
git submodule update --init
wget -O boost_1_76_0.tar.bz2 https://boostorg.jfrog.io/artifactory/main/release/1.76.0/source/boost_1_76_0.tar.bz2
tar xjf boost_1_76_0.tar.bz2
rm boost_1_76_0.tar.bz2
sudo apt-get install libsuitesparse-dev
```

Then setup the [Gurobi license](https://www.gurobi.com/downloads/end-user-license-agreement-academic/).

### Poetry
We use [poetry](https://python-poetry.org/docs/#installation) to manage our dependencies. 

## Installation

```bash
poetry install -E experiments -E test
poetry run pip install /path/to/dingo/root/directory
poetry run pip install -i https://pypi.gurobi.com gurobipy
```
