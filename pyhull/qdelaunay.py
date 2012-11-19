#!/usr/bin/env python

"""
This module implements a DelaunayTriangulation class.
"""

from __future__ import division

__author__ = "Shyue Ping Ong"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__status__ = "Beta"
__date__ = "Nov 19 2012"


import pyhull._pyhull as hull

from pyhull.simplex import Simplex

class DelaunayTriangulation(object):
    """
    Delaunay triangulation for a set of points.
    """

    def __init__(self, points):
        self.points = points
        self.vertices = self._calc_vertices(points)

    def _calc_vertices(self, points):
        """
        Returns the vertices of the Delaunay triangulation of a set of points.

        Args:
            points:
                All the points as a sequence of sequences. e.g., [[-0.5, -0.5],
                [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]

        Returns:
            The vertices as a list of list of integer indices. E.g., [[0, 2], [1,
            0], [2, 3], [3, 1]]
        """
        prep_str = [str(len(points[0])), str(len(points))]
        prep_str.extend([' '.join([str(i) for i in row]) for row in points])
        output = hull.qdelaunay("i", "\n".join(prep_str))
        output.pop(0)
        return [[int(i) for i in row.strip().split()] for row in output]

    @property
    def simplices(self):
        """
        Returns the simplices of the triangulation.
        """
        return [Simplex([self.points[i] for i in v]) for v in self.vertices]
