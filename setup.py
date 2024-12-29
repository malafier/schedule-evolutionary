from Cython.Build import cythonize
from setuptools import setup

setup(
    ext_modules=cythonize([
        "evolutionary/crossover_alg.pyx",
        "evolutionary/evaluation.pyx",
        "evolutionary/fixing_algorithm.pyx",
        "evolutionary/mutation.pyx",
    ]),
)
