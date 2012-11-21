#!/usr/bin/env python

"""
This module implements a VoronoiTess class representing a Voronoi tessellation
of a set of points.
"""

from __future__ import division

__author__ = "Shyue Ping Ong"
__version__ = "1.0"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__status__ = "Beta"
__date__ = "Nov 19 2012"

import itertools

import numpy as np

from pyhull import qvoronoi


class VoronoiTess(object):
    """
    Voronoi tessellation for a set of points.

    .. attribute: points

        Original points supplied.

    .. attribute: vertices

        Vertices of the Voronoi tessellation as a list of coords.
        E.g., [[-10.101, -10.101], [0.0, -0.5], [-0.5, 0.0], [0.5, 0.0],
        [0.0, 0.5]].
        Note that the value -10.101 is used by qhull to represent a point at
        infinity.

    .. attribute: regions

        Regions of the Voronoi tessellation as a list of vertex indices.
        E.g., [[4, 2, 1, 3], [2, 0, 1], [4, 0, 2], [3, 0, 1], [4, 0, 3]]

    .. attribute: ridges

        Ridges of the Voronoi tessellation as a dict of adjacent point
        indices to list of vertex indices.
        E.g., {(0, 1): [1, 2], (1, 2): [0, 2], (1, 3): [0, 1], (2, 4): [0, 4],
        (0, 4): [3, 4], (0, 3): [1, 3], (3, 4): [0, 3], (0, 2): [2, 4]}
        The key is a tuple of length 2 indicating the adjacent points. The
        values are a list of vertex indices. See the vertices attributes for
        the actual coordinates.
    """

    def __init__(self, points, add_bounding_box=False):
        """
        Args:
            points:
                All the points as a sequence of sequences. e.g., [[-0.5, -0.5],
                [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]
            add_bounding_box:
                If True, a hypercube corresponding to the extremes of each
                coordinate will be added to the list of points.
        """
        self.points = list(points)
        if add_bounding_box:
            coord_ranges = zip(np.amin(points, 0), np.amax(points, 0))
            for coord in itertools.product(*coord_ranges):
                self.points.append(coord)
        output = qvoronoi("o", self.points)
        output.pop(0)
        nvertices, nregions, i = map(int, output.pop(0).split())
        self.vertices = [[float(f) for f in output[i].split()]
                         for i in xrange(nvertices)]
        self.regions = [[int(j) for j in output[i].split()[1:]]
                         for i in xrange(nvertices, nvertices+nregions)]

        output = qvoronoi("Fv", self.points)
        output.pop(0)
        ridges = {}
        for line in output:
            val = map(int, line.split())
            ridges[tuple(val[1:3])] = val[3:]
        self.ridges = ridges
