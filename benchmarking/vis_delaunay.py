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

import itertools

import numpy as np

from pyhull.qdelaunay import DelaunayTriangulation
from pyhull.qconvex import ConvexHull
import matplotlib.pyplot as plt

points = np.random.randn(30, 2)
for pt in points:
    plt.plot(pt[0], pt[1], 'ro')


d = DelaunayTriangulation(points)

for s in d.simplices:
    for c1, c2 in itertools.combinations(s.coords, 2):
        plt.plot([c1[0],c2[0]], [c1[1], c2[1]], 'k-')

d = ConvexHull(points)

for s in d.simplices:
    for c1, c2 in itertools.combinations(s.coords, 2):
        plt.plot([c1[0],c2[0]], [c1[1], c2[1]], 'b-')

plt.show()
