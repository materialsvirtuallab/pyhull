__author__ = 'shyue'

import unittest
import numpy as np

from pyhull.qconvex import get_vertices

class FuncCase(unittest.TestCase):

    def test_get_vertices(self):
        data = [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5]]
        expected_ans = [[0, 2], [1, 0], [2, 3], [3, 1]]
        self.assertEqual(get_vertices(data), expected_ans)
        data.extend([[0, -0.5], [0,  0.5], [-0.5, 0], [0.5, 0]])
        self.assertEqual(get_vertices(data), expected_ans)

        print np.random.randn(100,3)
        print get_vertices(np.random.randn(100,3))

if __name__ == '__main__':
    unittest.main()
