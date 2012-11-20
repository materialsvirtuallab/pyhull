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


from pyhull import qdelaunay
from pyhull.simplex import Simplex


class DelaunayTri(object):
    """
    Delaunay triangulation for a set of points.

    .. attribute: points

        Original points supplied.

    .. attribute: vertices

        Vertices of the Delaunay triangulation as a list of list of integer
        indices. E.g., [[0, 2], [1, 0], [2, 3], [3, 1]]
    """

    def __init__(self, points):
        """
        Args:
            points:
            All the points as a sequence of sequences. e.g., [[-0.5, -0.5],
            [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]
        """
        self.points = points
        output = qdelaunay("i", points)
        output.pop(0)
        self.vertices = [[int(i) for i in row.strip().split()]
                         for row in output]

    @property
    def simplices(self):
        """
        Returns the simplices of the triangulation.
        """
        return [Simplex([self.points[i] for i in v]) for v in self.vertices]
