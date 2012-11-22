__author__ = 'shyue'

import unittest

import numpy as np

from pyhull.voronoi import VoronoiTess


class VoronoiTessTestCase(unittest.TestCase):

    def setUp(self):
        data = [[0,0], [-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]
        self.voro = VoronoiTess(data)
        sphere_data = [[0.3927286959385721, 0.3027233106882571,
                        -0.0642087887467873],
                       [-0.3040289937812381, 0.08411211324060132,
                        -0.3879323695524365],
                       [-0.4167147320140305, -0.1124203247935928,
                        0.252409395022804],
                       [-0.09784613055257477, 0.3994051836806832,
                        0.2844321254445218],
                       [0.0167085276338464, 0.4969839143091518,
                        0.05222847903455247],
                       [-0.3010383814570601, 0.3973744439739354,
                        0.03833332970300512],
                       [0.321916886905792, -0.3514017778986294,
                        -0.1512822144687402],
                       [-0.02357104947939958, 0.4654006301246191,
                        -0.1812364728912125],
                       [0.3199720537828011, -0.3299443654301472,
                        -0.1968618818332127],
                       [-0.4630278928730662, -0.1886147011806086,
                        0.005446551209538857]]
        self.spvoro = VoronoiTess(sphere_data)

        #Make sure higher dim works.
        points = np.random.randn(10, 5)
        self.hdvoro = VoronoiTess(points)

        #Check that bad points raises an error.
        bad_points = [[0,0], [0,1,0], [0,0]]
        self.assertRaises(ValueError, VoronoiTess, bad_points)

    def test_vertices(self):
        expected_ans = [[-10.101, -10.101], [0.0, -0.5], [-0.5, 0.0],
                        [0.5, 0.0], [0.0, 0.5]]
        self.assertEqual(self.voro.vertices, expected_ans)

    def test_regions(self):
        expected_ans = [[4, 2, 1, 3], [2, 0, 1], [4, 0, 2], [3, 0, 1],
                        [4, 0, 3]]

        self.assertEqual(self.voro.regions, expected_ans)
        #Sphere should always have a point at inf for all regions.
        for r in self.spvoro.regions:
            self.assertIn(0, r)

    def test_ridges(self):
        expected_ans = {(0, 1): [1, 2], (1, 2): [0, 2], (1, 3): [0, 1],
                        (2, 4): [0, 4], (0, 4): [3, 4], (0, 3): [1, 3],
                        (3, 4): [0, 3], (0, 2): [2, 4]}
        self.assertEqual(self.voro.ridges, expected_ans)

    def test_dim(self):
        self.assertEqual(self.voro.dim, 2)
        self.assertEqual(self.spvoro.dim, 3)

if __name__ == '__main__':
    unittest.main()
