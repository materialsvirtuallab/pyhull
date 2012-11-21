#!/usr/bin/env python

"""
Generates the Delaunay triangulation, Voronoi tessellation and convex hull for
a random set of 2D points and plot them. For testing purposes.

Red dots - random points.
Green lines - Delaunay triangulation.
Blue lines - convex hull.
Black lines - Voronoi tesselation.
Dash black lines - Voronoi tesselation with points at infinity.

"""

from __future__ import division

__author__ = "Shyue Ping Ong"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__status__ = "Beta"
__date__ = "11/19/12"

import itertools
import sys

import numpy as np

from pyhull.delaunay import DelaunayTri
from pyhull.convex_hull import ConvexHull
from pyhull.voronoi import VoronoiTess

import matplotlib.pyplot as plt

npts = int(sys.argv[1]) if len(sys.argv) > 1 else 30

points = np.random.randn(npts, 2)

legkeys = []
legitems = []

for pt in points:
    p, = plt.plot(pt[0], pt[1], 'ro')

legkeys.append(p)
legitems.append("Points")

d = DelaunayTri(points)

for s in d.simplices:
    for c1, c2 in itertools.combinations(s.coords, 2):
        p, = plt.plot([c1[0],c2[0]], [c1[1], c2[1]], 'g-')

legkeys.append(p)
legitems.append("Delaunay tri")

d = ConvexHull(points)

for s in d.simplices:
    for c1, c2 in itertools.combinations(s.coords, 2):
        p, = plt.plot([c1[0],c2[0]], [c1[1], c2[1]], 'b-')

legkeys.append(p)
legitems.append("Convex hull")

d = VoronoiTess(points)
points = d.points
avg = np.average(points, 0)
vertices = d.vertices
for nn, vind in d.ridges.items():
    (i1, i2) = sorted(vind)
    if i1 == 0:
        c1 = np.array(vertices[i2])
        midpt = 0.5 * (np.array(points[nn[0]]) + np.array(points[nn[1]]))
        if np.dot(avg - midpt, c1 - midpt)> 0:
            c2 = c1 + 10 * (midpt-c1)
        else:
            c2 = c1 - 10 * (midpt-c1)
        p1, = plt.plot([c1[0],c2[0]], [c1[1], c2[1]], 'k--')
    else:
        c1 = vertices[i1]
        c2 = vertices[i2]
        p, = plt.plot([c1[0],c2[0]], [c1[1], c2[1]], 'k-')

legkeys.append(p)
legitems.append("Voronoi tess.")
legkeys.append(p1)
legitems.append("Voronoi tess. - inf vert.")

#Set some sensible limits
maxc = np.amax(points, 0)
minc = np.amin(points, 0)
plt.xlim((minc[0]-0.1, maxc[0]+0.1))
plt.ylim((minc[1]-0.1, maxc[1]+0.1))

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 18}

plt.rc('font', **font)
#plt.legend(legkeys, legitems)
plt.show()
