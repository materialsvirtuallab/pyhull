#!/usr/bin/env python

"""
TODO: Change the module doc.
"""

from __future__ import division

__author__ = "shyuepingong"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__status__ = "Beta"
__date__ = "11/19/12"

import numpy as np

from scipy.spatial import Delaunay
from pyhull.qconvex import ConvexHull
from pymatgen.command_line.qhull_caller import qconvex

def scipy_test(data):
    return Delaunay(data).convex_hull

def pyhull_test(data):
    return ConvexHull(data)

def pymatgen_ext_test(data):
    return qconvex(data)

if __name__ == "__main__":
    import timeit
    global data
    for npts in [100, 1000, 2000]:
        for dim in [3,4,5,6]:
            print "Number of points: {}, Dim: {}".format(npts, dim)
            data = np.random.randn(npts,dim)
            print "Scipy: ",
            print timeit.timeit("scipy_test(data)",
                                setup="from __main__ import scipy_test, data",
                                number=1)
            print "pymatgen_ext_test: ",
            print timeit.timeit("pymatgen_ext_test(data)",
                                setup="from __main__ import pymatgen_ext_test, data",
                                number=1)
            print "pyhull: ",
            print timeit.timeit("pyhull_test(data)",
                                setup="from __main__ import pyhull_test, data",
                                number=1)