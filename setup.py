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

setup (name = 'pyhull',
       author="Shyue Ping Ong",
       author_email="shyuep@gmail.com",
       maintainer="Shyue Ping Ong",
       url="https://github.com/shyuep/pyhull",
       license="MIT",
       description = 'pyhull is a port of Qhull to Python.',
       keywords=["qhull", "convex", "hull", "computational",
                 "geometry"],
       classifiers=[
           "Programming Language :: Python :: 2.7",
           "Development Status :: 4 - Beta",
           "Intended Audience :: Science/Research",
           "License :: OSI Approved :: MIT License",
           "Operating System :: OS Independent",
           "Topic :: Software Development :: Libraries :: Python Modules"
       ],
       download_url="https://github.com/shyuep/pyhull/archive/master.tar.gz",
       packages=find_packages(),
       version = '0.1',
       ext_modules = [extension]
)