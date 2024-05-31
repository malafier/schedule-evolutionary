from Cython.Build import cythonize
from setuptools import setup

setup(
    ext_modules=cythonize(["evolutionary/crossover.pyx", "evolutionary/evaluation.pyx"]),
)
