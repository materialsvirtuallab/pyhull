__author__ = 'shyue'

import unittest

from pyhull import qconvex, qdelaunay, qvoronoi


class FuncCase(unittest.TestCase):

    def test_qconvex(self):
        data = [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]
        self.assertEqual(['4', '0 2', '1 0', '2 3', '3 1'],
                         qconvex("i", data))
        self.assertEqual(['4', '0 2', '1 0', '2 3', '3 1'],
                         qconvex("i Qt", data))
        self.assertEqual(qconvex("n", data), ['3', '4',
                                              '-0     -1   -0.5',
                                              '-1      0   -0.5',
                                              '1     -0   -0.5',
                                              '0      1   -0.5'])
        self.assertIsNotNone(qconvex('QR0 FA Pp', data))


    def test_qdelaunay(self):
        data = [[0,0], [-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]
        self.assertEqual(['4', '3 0 1', '0 2 1', '4 0 3', '0 4 2'],
                         qdelaunay("i", data))
        self.assertEqual(qdelaunay("n", data),
                         ['4', '4',
                          '-0 -0.8944271909999159 -0.4472135954999579      0',
                          '-0.8944271909999159      0 -0.4472135954999579     -0',
                          '0.8944271909999159      0 -0.4472135954999579     -0',
                          '-0 0.8944271909999159 -0.4472135954999579     -0']
        )
        self.assertEqual(qdelaunay("i n", data),
                         ['4', '3 0 1', '0 2 1', '4 0 3', '0 4 2',
                          '4', '4',
                          '-0 -0.8944271909999159 -0.4472135954999579      0',
                          '-0.8944271909999159      0 -0.4472135954999579     -0',
                          '0.8944271909999159      0 -0.4472135954999579     -0',
                          '-0 0.8944271909999159 -0.4472135954999579     -0']
        )


    def test_qvoronoi(self):
        data = [[0,0], [-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]
        self.assertEqual(['2', '4', '0   -0.5', '-0.5      0',
                          '0.5      0', '0    0.5'],
                         qvoronoi("p", data))
        self.assertEqual(['2', '5 5 1', '-10.101 -10.101',
                          '0   -0.5', '-0.5      0',
                          '0.5      0', '0    0.5', '4 4 2 1 3',
                          '3 2 0 1', '3 4 0 2', '3 3 0 1', '3 4 0 3',
                          '2', '4', '0   -0.5', '-0.5      0',
                          '0.5      0', '0    0.5'],
                         qvoronoi("o p", data))


if __name__ == '__main__':
    unittest.main()
