#!/usr/bin/env python

from __future__ import division

__author__ = "Will Richards"
__version__ = "2.0"
__maintainer__ = "Will Richards"
__email__ = "wrichard@mit.edu"
__date__ = "August 2, 2013"

import unittest
import numpy as np

from pyhull.halfspace import Halfspace, HalfspaceIntersection

class HalfspaceTest(unittest.TestCase):

    def test_halfspace(self):
        h1 = Halfspace.from_hyperplane([[0,1,0], [1,0,0]], [1,1,-100], [2,2,2], True)
        self.assertTrue(all(h1.normal == [0,0,-1]))
        self.assertEqual(h1.offset, -100)
        h2 = Halfspace.from_hyperplane([[0,1,0], [1,0,0]], [1,1,-100], [2,2,2], False)
        self.assertEqual(h2.offset, 100)

    def test_intersection(self):
        h1 = Halfspace.from_hyperplane([[1,0,0], [0,1,0]], [1,1,1], [0.9, 0.9, 0.9], True)
        h2 = Halfspace.from_hyperplane([[0,1,0], [0,0,1]], [1,1,1], [0.9, 0.9, 0.9], True)
        h3 = Halfspace.from_hyperplane([[0,0,1], [1,0,0]], [1,1,1], [0.9, 0.9, 0.9], True)
        h4 = Halfspace.from_hyperplane([[-1,0,1], [0,-1,1]], [1,1,0], [0.9, 0.9, 0.9], True)

        hi = HalfspaceIntersection([h1, h2, h3, h4], [0.9, 0.9, 0.9])
        self.assertTrue(np.allclose(np.sum(hi.vertices, axis = 0), [3,3,3]))

        h5 = Halfspace.from_hyperplane([[1,0,0], [0,1,0]], [1,2,2], [0.9, 0.9, 0.9], True)
        hi = HalfspaceIntersection([h5, h2, h3, h4], [0.9, 0.9, 0.9])
        self.assertTrue(np.allclose(np.sum(hi.vertices, axis = 0), [2,2,6]))

        for h, vs in zip(hi.halfspaces, hi.facets_by_halfspace):
            for v in vs:
                self.assertAlmostEqual(np.dot(h.normal, hi.vertices[v]) + h.offset, 0)
        for v, hss in zip(hi.vertices, hi.facets_by_vertex):
            for i in hss:
                hs = hi.halfspaces[i]
                self.assertAlmostEqual(np.dot(hs.normal, v) + hs.offset, 0)

    def test_intersection2d(self):
        h1 = Halfspace([1,0], -1)
        h2 = Halfspace([0,1], 1)
        h3 = Halfspace([-2,-1], 0)
        h_redundant = Halfspace([1,0], -2)
        hi = HalfspaceIntersection([h1, h2, h_redundant, h3], [0.9,-1.1])

        for h, vs in zip(hi.halfspaces, hi.facets_by_halfspace):
            for v in vs:
                self.assertAlmostEqual(np.dot(h.normal, hi.vertices[v]) + h.offset, 0)
        for v, hss in zip(hi.vertices, hi.facets_by_vertex):
            for i in hss:
                hs = hi.halfspaces[i]
                self.assertAlmostEqual(np.dot(hs.normal, v) + hs.offset, 0)

        #redundant halfspace should have no vertices
        self.assertEqual(len(hi.facets_by_halfspace[2]), 0)

        self.assertTrue(np.any(np.all(hi.vertices == np.array([1,-2]), axis=1)))
        self.assertTrue(np.any(np.all(hi.vertices == np.array([1,-1]), axis=1)))

    def test_infinite_vertex(self):
        h1 = Halfspace.from_hyperplane([[1,0,0], [0,1,0]], [1,1,1], [0.9, 0.9, 0.9], True)
        h2 = Halfspace.from_hyperplane([[0,1,0], [0,0,1]], [1,1,1], [0.9, 0.9, 0.9], True)
        h3 = Halfspace.from_hyperplane([[0,0,1], [1,0,0]], [1,1,1], [0.9, 0.9, 0.9], True)
        h4 = Halfspace.from_hyperplane([[1,0,0], [0,1,0]], [2,2,2], [0.9, 0.9, 0.9], True)

        hi = HalfspaceIntersection([h1, h2, h3, h4], [0.9, 0.9, 0.9])
        self.assertTrue(np.allclose(np.sum(hi.vertices, axis = 0), [np.inf,np.inf,np.inf]))

    def test_non_unit_normals(self):
        h1 = Halfspace([3,0], -3)
        h2 = Halfspace([0,2], 2)
        h3 = Halfspace([-2,-1], 0)
        hi = HalfspaceIntersection([h1, h2, h3], [0.9,-1.1])
        self.assertTrue(np.any(np.all(hi.vertices == np.array([1,-2]), axis=1)))
        self.assertTrue(np.any(np.all(hi.vertices == np.array([1,-1]), axis=1)))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
