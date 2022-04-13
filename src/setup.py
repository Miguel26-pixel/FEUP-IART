from setuptools import setup
from Cython.Build import cythonize


setup(
    name='IART',
    version='1.0',
    description='Hashcode Streetview Routing',
    author='Group',
    ext_modules=cythonize(["./*/*.py","main.py"], compiler_directives={'language_level' : "3"}, exclude=["testing/crossover.py"])
)
