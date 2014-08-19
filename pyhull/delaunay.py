"""
This module implements a DelaunayTri class representing a Delaunay
triangulation of a set of points.
"""

from __future__ import division

__author__ = "Shyue Ping Ong"
__version__ = "1.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__status__ = "Production"
__date__ = "Nov 19 2012"


from pyhull import qdelaunay
from pyhull.simplex import Simplex


class DelaunayTri(object):
    """
    Delaunay triangulation for a set of points.

    .. attribute: dim

        Dimension of the points.

    .. attribute: points

        Original points supplied.

    .. attribute: vertices

        Vertices of the Delaunay triangulation as a list of list of integer
        indices. E.g., [[0, 2], [1, 0], [2, 3], [3, 1]]
    """

    def __init__(self, points, joggle=False):
        """
        Initializes a DelaunayTri from points.

        Args:
            points ([[float]]): All the points as a sequence of sequences.
                e.g., [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]
            joggle (bool): Use qhull option to joggle inputs until simplical
                result is obtained instead of merging facets.
        """
        self.points = points
        dim = map(len, self.points)
        if max(dim) != min(dim):
            raise ValueError("Input points must all have the same dimension!")
        self.dim = dim[0]
        if joggle:
            options = "i QJ"
        else:
            options = "i Qt"
        output = qdelaunay(options, points)
        output.pop(0)
        self.vertices = [map(int, row.strip().split()) for row in output]

    @property
    def simplices(self):
        """
        Returns the simplices of the triangulation.
        """
        return [Simplex([self.points[i] for i in v]) for v in self.vertices]
