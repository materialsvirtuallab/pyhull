#!/usr/bin/env python

"""
Script to perform a scaling benchmark.
"""

from __future__ import division

__author__ = "shyuepingong"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__status__ = "Beta"
__date__ = "11/19/12"

import numpy as np
import itertools
import collections
from pyhull.convex_hull import ConvexHull
from pyhull.delaunay import DelaunayTri
from pyhull.voronoi import VoronoiTess
import matplotlib.pyplot as plt

def pyhull_test(cls, npts, dim):
    data = np.random.randn(npts, dim)
    return cls(data)


if __name__ == "__main__":
    import timeit
    classes = ["VoronoiTess"]
    dims = [2, 3, 4]
    numpts = [10, 100, 1000, 5000, 10000]
    stats = collections.defaultdict(dict)
    for cls, dim, npts in itertools.product(classes, dims, numpts):
        if not (cls in ["DelaunayTr", "VoronoiTess"] and dim == 7):
            t = timeit.timeit("pyhull_test({}, {}, {})".format(cls, npts, dim),
                              setup="from __main__ import pyhull_test, {}".format(cls),
                              number=5)
            print "{}, npts = {}, dim = {}, time = {}".format(cls, npts, dim, t/5)
            stats[cls][(dim, npts)] = t/5

    colors = ['r', 'g', 'b', 'k', 'm']
    styles = ['-', '-.', '--']
    symbols = ['o', 's', 'p']
    for k, v in stats.items():
        for dim in dims:
            if not (k in ["DelaunayTr", "VoronoiTess"] and dim == 7):
                data = [(k2[1], v2) for k2, v2 in v.items() if k2[0] == dim]
                data = sorted(data, key=lambda x: x[0])
                col = colors[dims.index(dim)]
                sty = styles[classes.index(k)]
                sym = symbols[classes.index(k)]

                plt.plot([x[0] for x in data], [x[1] for x in data],
                         '{}{}{}'.format(col, sty, sym), markersize=10,
                         linewidth=3, label="{} - {}D".format(k, dim))
    plt.legend(loc='upper left', prop={'size':20})

    font = {'family': 'Times New Roman', 'size': 18}
    plt.rc('font', **font)
    plt.ylabel("Time (seconds)")
    plt.xlabel("Number of points")
    plt.show()

