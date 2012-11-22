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
Pyhull is a Python wrapper to Qhull (http://www.qhull.org/) for the
computation of the convex hull, Delaunay triangulation and Voronoi diagram.
It is written as a Python C extension, with both high-level and low-level
interfaces to qhull.

Currently, there is no effective port of the qhull algorithm,
especially for higher dimensions. While isolated packages exist
for up to 3D convex hulls, no effective package exist for higher dimensions.
The only other known code which supports convex hulls in higher dimensions is
the scipy.spatial package, but that code is extremely inefficient compared to
the original Qhull in C. Pyhull is much faster than the scipy.spatial package.

Pyhull has been tested to scale to 10,000 7D points for convex hull
calculations (results in ~ 10 seconds), and 10,000 6D points for Delaunay
triangulations and Voronoi tesselations (~ 100 seconds). Higher number of
points and higher dimensions should be accessible depending on your machine,
but may take a significant amount of time.

For more details or to report bugs, please visit the pyhull GitHub page at
https://github.com/shyuep/pyhull or the documentation page at
http://packages.python.org/pyhull/.
"""

setup (name = 'pyhull',
       version = '1.3',
       author="Shyue Ping Ong",
       author_email="shyuep@gmail.com",
       maintainer="Shyue Ping Ong",
       url="https://github.com/shyuep/pyhull",
       license="MIT",
       description = 'A Python wrapper to Qhull (http://www.qhull.org/) for '
                     'the computation of the convex hull, '
                     'Delaunay triangulation and Voronoi diagram',
       keywords=["qhull", "convex", "hull", "computational",
                 "geometry", "delaunay", "triangulation", "voronoi",
                 "diagram"],
       install_requires=["numpy>=1.5"],
       classifiers=[
           "Programming Language :: Python :: 2.7",
           "Development Status :: 5 - Production/Stable",
           "Intended Audience :: Science/Research",
           "License :: OSI Approved :: MIT License",
           "Operating System :: OS Independent",
           "Topic :: Software Development :: Libraries :: Python Modules",
           "Topic :: Scientific/Engineering :: Mathematics"
       ],
       long_description=long_description,
       download_url="https://github.com/shyuep/pyhull/archive/master.tar.gz",
       packages=find_packages(),
       ext_modules = [extension]
)