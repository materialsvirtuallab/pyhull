__author__ = 'shyue'

import glob
import os
from distribute_setup import use_setuptools
use_setuptools(version='0.6.10')
from setuptools import setup, Extension, find_packages

src_dir = "src"
include_dirs = glob.glob(os.path.join("src", "libqhull"))
sources = glob.glob(os.path.join("src", "libqhull", "*.c"))
extension = Extension('pyhull._pyhull',
                      include_dirs=include_dirs,
                      sources=['_pyhull.c'] + sources
)

long_description = """
pyhull is a Python wrapper to Qhull (http://www.qhull.org/) for the
computation of the convex hull, Delaunay triangulation and Voronoi diagram.
It is written as a Python C extension, with both high-level and low-level
interfaces to qhull.

Currently, there is no effective port of the qhull algorithm,
especially for higher dimensions. While isolated packages exist
for up to 3D convex hulls, no effective package exist for higher dimensions.
The only other known code which supports convex hulls in higher dimension is
the scipy.spatial package, but that code is extremely inefficient compared to
the original Qhull in C. Pyhull is much faster than the scipy.spatial package.

For more details, please visit the pyhull GitHub page at
https://github.com/shyuep/pyhull.
"""

setup (name = 'pyhull',
       version = '1.0',
       author="Shyue Ping Ong",
       author_email="shyuep@gmail.com",
       maintainer="Shyue Ping Ong",
       url="https://github.com/shyuep/pyhull",
       license="MIT",
       description = 'pyhull is a port of Qhull to Python.',
       keywords=["qhull", "convex", "hull", "computational",
                 "geometry"],
       install_requires=["numpy>=1.5"],
       classifiers=[
           "Programming Language :: Python :: 2.7",
           "Development Status :: 4 - Beta",
           "Intended Audience :: Science/Research",
           "License :: OSI Approved :: MIT License",
           "Operating System :: OS Independent",
           "Topic :: Software Development :: Libraries :: Python Modules"
       ],
       long_description=long_description,
       download_url="https://github.com/shyuep/pyhull/archive/master.tar.gz",
       packages=find_packages(),
       ext_modules = [extension]
)