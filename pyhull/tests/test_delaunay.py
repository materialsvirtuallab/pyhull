__author__ = 'shyue'

import unittest

import numpy as np

from pyhull.delaunay import DelaunayTri


class DelaunayTriTestCase(unittest.TestCase):

    def setUp(self):
        data = [[0,0], [-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]
        self.delau = DelaunayTri(data)
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
        self.spdelau = DelaunayTri(sphere_data)

        #Make sure higher dim works.
        points = np.random.randn(10, 5)
        self.hddelau = DelaunayTri(points)

        #Check that bad points raises an error.
        bad_points = [[0,0], [0,1,0], [0,0]]
        self.assertRaises(ValueError, DelaunayTri, bad_points)

    def test_vertices(self):
        expected_ans = [[3, 0, 1], [0, 2, 1], [4, 0, 3], [0, 4, 2]]
        self.assertEqual(self.delau.vertices, expected_ans)
        expected_ans = [[1, 3, 6, 0], [1, 8, 6, 9], [8, 1, 6, 0], [2, 5, 1, 9],
                        [2, 5, 3, 1], [2, 1, 6, 9], [3, 2, 1, 6], [7, 3, 1, 0],
                        [5, 7, 3, 1], [7, 4, 3, 0], [7, 4, 5, 3]]
        print self.spdelau.vertices
        self.assertEqual(self.spdelau.vertices, expected_ans)

    def test_simplices(self):
        self.assertEqual(len(self.delau.simplices), 4)
        self.assertEqual(len(self.spdelau.simplices), 11)

    def test_dim(self):
        self.assertEqual(self.delau.dim, 2)
        self.assertEqual(self.spdelau.dim, 3)

    def test_joggle(self):
        joggled_delau = DelaunayTri(self.delau.points, joggle=True)
        expected_ans = set([(0, 1, 3), (0, 1, 2), (0, 3, 4), (0, 2, 4)])
        ans = set([tuple(sorted(x)) for x in joggled_delau.vertices])
        self.assertEqual(ans, expected_ans)


if __name__ == '__main__':
    unittest.main()
