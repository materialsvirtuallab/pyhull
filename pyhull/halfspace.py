"""
This module defines classes for computing halfspace intersections
"""

from __future__ import division

__author__ = "Will Richards"
__version__ = "2.0"
__maintainer__ = "Will Richards"
__email__ = "wrichard@mit.edu"
__date__ = "August 2, 2013"

from pyhull import qhalf

import numpy as np

class Halfspace(object):
    """
    A halfspace defined by dot(normal, coords) + offset <= 0
    """
    def __init__(self, normal, offset):
        """
        Initializes a Halfspace.

        Args:
            normal: vector normal to hyperplane
            offset: offset of hyperplane from origin
        """
        self.normal = normal
        self.offset = offset

    def __str__(self):
        return "Halfspace, normal: {}, offset: {}".format(self.normal, self.offset)

    @staticmethod
    def from_hyperplane(basis, origin, point, internal = True):
        """
        Returns a Halfspace defined by a list of vectors parallel to the
        bounding hyperplane.

        Args:
            basis: basis for the hyperplane (array with vector rows)
            origin: point on the hyperplane
            point: point not on the hyperplane
            internal: whether point is inside the halfspace
        """
        basis = np.array(basis)
        assert basis.shape[0] + 1 == basis.shape[1]

        big_basis = np.zeros((basis.shape[1], basis.shape[1]))
        big_basis[:basis.shape[0],:basis.shape[1]] = basis

        u, s, vh = np.linalg.svd(big_basis)
        null_mask = (s <= 1e-8)
        normal = np.compress(null_mask, vh, axis=0)[0]

        if np.inner(np.array(point)-np.array(origin), normal) > 0:
            if internal:
                normal *= -1
        else:
            if not internal:
                normal *= -1
        offset = -np.dot(origin, normal)
        return Halfspace(normal, offset)


class HalfspaceIntersection(object):
    """
    Uses qhalf to calculate the vertex representation of the intersection
    of a set of halfspaces
    """
    def __init__(self, halfspaces, interior_point):
        self.halfspaces = halfspaces
        self.interior_point = interior_point
        self._v_out = None
        self._fbv_out = None
        self._fbh_out = None

    @property
    def vertices(self):
        """
        Returns the vertices of the halfspace intersection
        """
        if self._v_out is None:
            output = qhalf('Fp', self.halfspaces, self.interior_point)
            pts = []
            for l in output[2:]:
                pt = []
                for c in l.split():
                    c = float(c)
                    if c != 10.101 and c != -10.101:
                        pt.append(c)
                    else:
                        pt.append(np.inf)
                pts.append(pt)
            self._v_out = np.array(pts)
        return self._v_out

    @property
    def facets_by_vertex(self):
        """
        Returns a list of non-redundant halfspace indices for each vertex
        e.g: facets_by_vertex[0] is the list of indices of halfspaces
        incident to vertex 0
        """
        if self._fbv_out is None:
            output = qhalf('Fv', self.halfspaces, self.interior_point)
            facets = []
            for l in output[1:]:
                facets.append([int(i) for i in l.split()[1:]])
            self._fbv_out = facets
        return self._fbv_out

    @property
    def facets_by_halfspace(self):
        """
        Returns a list of vertex indices for each halfspace
        e.g: facets_by_halfspace[0] is the list of indices ov vertices
        incident to halfspace 0
        """
        if self._fbh_out is None:
            output = qhalf('FN', self.halfspaces, self.interior_point)
            facets = []
            for l in output[1:]:
                facets.append([int(i) for i in l.split()[1:]])
            self._fbh_out = facets
        return self._fbh_out


