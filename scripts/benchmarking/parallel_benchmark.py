#!/usr/bin/env python

"""
TODO: Change the module doc.
"""

from __future__ import division

__author__ = "Shyue Ping Ong"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__status__ = "Beta"
__date__ = "11/19/12"

from multiprocessing import Pool

import numpy as np

from pyhull.convex_hull import ConvexHull

num_proc = 100

def get_vertices(data):
    return ConvexHull(data).vertices

def serial_test(data):
    d = []
    for i in xrange(num_proc):
        d.append(get_vertices(data))
    return d

def parallel_test(data):
    p = Pool(4)
    all_data = p.map(get_vertices, [data] * num_proc)
    assert all([all_data[i] == all_data[0] for i in xrange(num_proc)])

if __name__ == "__main__":
    import timeit
    global data
    for npts in [100, 1000, 10000]:
        for dim in [3, 4, 5]:
            data = np.random.randn(npts,dim)
            t = timeit.timeit("serial_test(data)",
                              setup="from __main__ import serial_test, data",
                              number=1)
            print ("Serial:   {} {} {:.5f}".format(npts, dim, t))
            t = timeit.timeit("parallel_test(data)",
                              setup="from __main__ import parallel_test, data",
                              number=1)
            print ("Parallel: {} {} {:.5f}".format(npts, dim, t))
