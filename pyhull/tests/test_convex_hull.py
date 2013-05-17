__author__ = 'shyue'

import unittest
import numpy as np


from pyhull.convex_hull import ConvexHull

class ConvexHullTestCase(unittest.TestCase):

    def setUp(self):
        data = [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]
        self.hull = ConvexHull(data)
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
        self.sphull = ConvexHull(sphere_data)

        #Make sure higher dim works.
        points = np.random.randn(10, 5)
        self.hdhull = ConvexHull(points)

        #Check that bad points raises an error.
        bad_points = [[0,0], [0,1,0], [0,0]]
        self.assertRaises(ValueError, ConvexHull, bad_points)

    def test_vertices(self):
        expected_ans = [[0, 2], [1, 0], [2, 3], [3, 1]]
        self.assertEqual(self.hull.vertices, expected_ans)
        expected_ans = [[1, 5, 9], [6, 3, 0], [6, 8, 9], [8, 1, 9], [8, 6, 0],
                        [1, 8, 0], [7, 1, 0], [7, 5, 1], [2, 6, 9], [2, 3, 6],
                        [5, 2, 9], [3, 2, 5], [4, 3, 5], [7, 4, 5], [3, 4, 0],
                        [4, 7, 0]]
        self.assertEqual(self.sphull.vertices, expected_ans)
        
    def test_joggle(self):
        joggled_hull = ConvexHull(self.hull.points, joggle=True)
        expected_ans = set([(0, 2), (1, 0), (2, 3), (3, 1)])
        ans = set([tuple(x) for x in joggled_hull.vertices])
        self.assertEqual(ans, expected_ans)
        joggled_sphull = ConvexHull(self.sphull.points, joggle=True)
        expected_ans = set([(1, 5, 9), (6, 3, 0), (6, 8, 9), (8, 1, 9), (8, 6, 0),
                            (1, 8, 0), (7, 1, 0), (7, 5, 1), (2, 6, 9), (2, 3, 6),
                            (5, 2, 9), (3, 2, 5), (4, 3, 5), (7, 4, 5), (3, 4, 0),
                            (4, 7, 0)])
        ans = set([tuple(x) for x in joggled_sphull.vertices])
        self.assertEqual(ans, expected_ans)

    def test_redundant_points(self):
        data = self.hull.points
        expected_ans = [[0, 2], [1, 0], [2, 3], [3, 1]]
        data.extend([[0, -0.5], [0,  0.5], [-0.5, 0], [0.5, 0]])
        self.assertEqual(ConvexHull(data).vertices, expected_ans)

    def test_simplices(self):
        self.assertEqual(len(self.hull.simplices), 4)
        self.assertEqual(len(self.sphull.simplices), 16)

    def test_dim(self):
        self.assertEqual(self.hull.dim, 2)
        self.assertEqual(self.sphull.dim, 3)

if __name__ == '__main__':
    unittest.main()
