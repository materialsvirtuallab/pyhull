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

from scipy.spatial import ConvexHull as CHullSci
from pyhull.convex_hull import ConvexHull as CHullPyhull

def scipy_test(data):
    return CHullSci(data)


def pyhull_test(data):
    return CHullPyhull(data)


if __name__ == "__main__":
    import timeit

    global data
    output = ["<table>", "<tr><th>Number of points</th>",
              "<th>Dim</th><th>scipy</th>",
              "<th>pyhull</th>"]
    for npts in [100, 1000, 2000]:
        for dim in [3, 4, 5, 6]:
            row = []
            row.append("{:5d}".format(npts))
            row.append("{:3d}".format(dim))
            data = np.random.randn(npts, dim)
            t = timeit.timeit("scipy_test(data)",
                              setup="from __main__ import scipy_test, data",
                              number=1)
            row.append("{:.5f}".format(t))
            t = timeit.timeit("pyhull_test(data)",
                              setup="from __main__ import pyhull_test, data",
                              number=1)
            row.append("{:.5f}".format(t))
            print " ".join(row)
    print "\n".join(output)