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
import argparse

import numpy as np

from pyhull.delaunay import DelaunayTri
from pyhull.convex_hull import ConvexHull
from pyhull.voronoi import VoronoiTess

import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description="Demo script for pyhull.",
                                 epilog="Author: Shyue Ping Ong")

parser.add_argument("-d", "--dimension", dest="dim", type=int,
                            choices=[2, 3],
                            default=2,
                            help="Dimension of points.")

parser.add_argument("-n", "--npoints", dest="npts", type=int,
                    default=30,
                    help="Number of points.")

args = parser.parse_args()

npts = args.npts
dim = args.dim

points = np.random.randn(npts, dim)

legkeys = []
legitems = []

if dim == 3:
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

for pt in points:
    p, = plt.plot(pt[0], pt[1], 'ro') if dim == 2 \
        else plt.plot([pt[0]], [pt[1]], [pt[2]], 'ro')

legkeys.append(p)
legitems.append("Points")

d = DelaunayTri(points)

for s in d.simplices:
    for data in itertools.combinations(s.coords, dim):
        data = np.array(data)
        p, = plt.plot(data[:,0], data[:,1], 'g-') if dim == 2 else\
            ax.plot(data[:,0], data[:,1], data[:,2], 'g-')

legkeys.append(p)
legitems.append("Delaunay tri")

d = ConvexHull(points)

for s in d.simplices:
    for data in itertools.combinations(s.coords, dim):
        data = np.array(data)
        p, = plt.plot(data[:,0], data[:,1], 'b-') if dim == 2 else\
            ax.plot(data[:,0], data[:,1], data[:,2], 'b-')

legkeys.append(p)
legitems.append("Convex hull")

if dim == 2:
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

font = {'family' : 'Times New Roman',
        'size'   : 18}

plt.rc('font', **font)
plt.show()
