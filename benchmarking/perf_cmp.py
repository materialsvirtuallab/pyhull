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
from pyhull.qconvex import get_vertices
from pymatgen.command_line.qhull_caller import qconvex


data = np.random.randn(100,3)

def scipy_test():
    return Delaunay(data).convex_hull

def pyhull_test():
    return get_vertices(data)

def pymatgen_ext_test():
    return qconvex(data)

if __name__ == "__main__":
    import timeit
    print "Scipy results"
    print timeit.timeit("scipy_test()",
                        setup="from __main__ import scipy_test",
                        number=1)
    print
    print "pymatgen_ext_test results"
    print timeit.timeit("pymatgen_ext_test()",
                        setup="from __main__ import pymatgen_ext_test",
                        number=1)
    print
    print "pyhull results"
    print timeit.timeit("pyhull_test()",
                        setup="from __main__ import pyhull_test",
                        number=1)
    print