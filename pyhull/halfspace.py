from __future__ import division
from pyhull import qhalf
import numpy as np

class Halfspace(object):
    '''
    A halfspace defined by dot(normal, coords) + offset <= 0 
    '''
    def __init__(self, normal, offset):
        self.normal = normal
        self.offset = offset
    
    def __str__(self):
        return "Halfspace, normal: {}, offset: {}".format(self.normal, self.offset)
        
    @staticmethod
    def from_hyperplane(basis, origin, point, internal = True):
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
        offset = -np.inner(origin, normal)
        return Halfspace(normal, offset)
    
class HalfspaceIntersection(object):
    def __init__(self, halfspaces, interior_point):
        self.halfspaces = halfspaces
        output = qhalf('Fp', halfspaces, interior_point)
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
        self.vertices = np.array(pts)
