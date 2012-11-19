pyhull
=======

pyhull is a port of Qhull as a Python extension. It is currently in an
extremely early alpha, and only a very limited subset of functions are
supported.

The reason for this package is that there is currently no effective port of
the qhull, especially for higher dimensions. While isolated packages exist
for up to 3D convex hulls, no effective package exist for higher dimensions.
The only other known code which supports convex hulls in higher dimension is
the scipy.spatial package, but that code is extremely inefficient compared to
 the original Qhull in C. (see below for performance details).

Performance of pyhull
=====================

pyqhull is still in the early stages of development, but some performance
metrics are already available.

Time taken to generate convex hull
----------------------------------

Number of points: 100, Dim: 3
Scipy:  0.00206589698792
External qconvex call:  0.00959587097168
pyhull:  0.00226211547852

Number of points: 100, Dim: 4
Scipy:  0.00648903846741
External qconvex call:  0.010675907135
pyhull:  0.00255990028381

Number of points: 100, Dim: 5
Scipy:  0.0293080806732
External qconvex call:  0.0185289382935
pyhull:  0.0130131244659

Number of points: 100, Dim: 6
Scipy:  0.172260046005
External qconvex call:  0.0414488315582
pyhull:  0.0366990566254

Number of points: 1000, Dim: 3
Scipy:  0.0175380706787
External qconvex call:  0.0127100944519
pyhull:  0.00764417648315

Number of points: 1000, Dim: 4
Scipy:  0.153062105179
External qconvex call:  0.0193359851837
pyhull:  0.0124320983887

Number of points: 1000, Dim: 5
Scipy:  1.01452088356
External qconvex call:  0.0441119670868
pyhull:  0.0399751663208

Number of points: 1000, Dim: 6
Scipy:  8.98945713043
External qconvex call:  0.287966966629
pyhull:  0.262745141983

Number of points: 2000, Dim: 3
Scipy:  0.0420558452606
External qconvex call:  0.0209732055664
pyhull:  0.0152490139008

Number of points: 2000, Dim: 4
Scipy:  0.32099199295
External qconvex call:  0.0300571918488
pyhull:  0.0222969055176

Number of points: 2000, Dim: 5
Scipy:  2.37638711929
External qconvex call:  0.0631880760193
pyhull:  0.0569159984589

Number of points: 2000, Dim: 6
Scipy:  27.925194025
External qconvex call:  0.519797086716
pyhull:  0.496487855911