__author__ = 'shyue'

import unittest

from pyhull import qconvex, qdelaunay, qvoronoi


class FuncCase(unittest.TestCase):

    def test_qconvex(self):
        data = [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]
        self.assertEqual(['4\n', '0 2 \n', '1 0 \n', '2 3 \n', '3 1 \n'],
                         qconvex("i", data))
        self.assertEqual(['4\n', '0 2 \n', '1 0 \n', '2 3 \n', '3 1 \n'],
                         qconvex("i Qt", data))
        self.assertEqual(qconvex("n", data), ['3\n', '4\n',
                                              '    -0     -1   -0.5 \n',
                                              '    -1      0   -0.5 \n',
                                              '     1     -0   -0.5 \n',
                                              '     0      1   -0.5 \n'])

    def test_qdelaunay(self):
        data = [[0,0], [-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]
        self.assertEqual(['4\n', '3 0 1 \n', '0 2 1 \n', '4 0 3 \n',
                          '0 4 2 \n'],
                         qdelaunay("i", data))
        self.assertEqual(qdelaunay("n", data),
                         ['4\n', '4\n',
                          '    -0 -0.8944271909999159 -0.4472135954999579      0 \n',
                          '-0.8944271909999159      0 -0.4472135954999579     -0 \n',
                          '0.8944271909999159      0 -0.4472135954999579     -0 \n',
                          '    -0 0.8944271909999159 -0.4472135954999579     -0 \n']
        )
        self.assertEqual(qdelaunay("i n", data),
                         ['4\n', '3 0 1 \n', '0 2 1 \n', '4 0 3 \n', '0 4 2 \n',
                          '4\n', '4\n',
                          '    -0 -0.8944271909999159 -0.4472135954999579      0 \n',
                          '-0.8944271909999159      0 -0.4472135954999579     -0 \n',
                          '0.8944271909999159      0 -0.4472135954999579     -0 \n',
                          '    -0 0.8944271909999159 -0.4472135954999579     -0 \n']
        )


    def test_qvoronoi(self):
        data = [[0,0], [-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]
        self.assertEqual(['2\n', '4\n', '     0   -0.5 \n', '  -0.5      0 \n',
                          '   0.5      0 \n', '     0    0.5 \n'],
                         qvoronoi("p", data))
        self.assertEqual(['2\n', '5 5 1\n', '-10.101 -10.101 \n',
                          '     0   -0.5 \n', '  -0.5      0 \n',
                          '   0.5      0 \n', '     0    0.5 \n', '4 4 2 1 3\n',
                          '3 2 0 1\n', '3 4 0 2\n', '3 3 0 1\n', '3 4 0 3\n',
                          '2\n', '4\n', '     0   -0.5 \n', '  -0.5      0 \n',
                          '   0.5      0 \n', '     0    0.5 \n'],
                         qvoronoi("o p", data))


if __name__ == '__main__':
    unittest.main()
