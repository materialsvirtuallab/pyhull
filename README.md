pyhull
=======

pyhull is a port of Qhull (http://www.qhull.org/) as a Python extension. It
is currently in an extremely early alpha, and only a very limited subset of
functions are supported.

The reason for this package is that there is currently no effective port of
the qhull, especially for higher dimensions. While isolated packages exist
for up to 3D convex hulls, no effective package exist for higher dimensions.
The only other known code which supports convex hulls in higher dimension is
the scipy.spatial package, but that code is extremely inefficient compared to
 the original Qhull in C. (see below for performance details).

Performance of pyhull
=====================

pyhull is still in the early stages of development, but some performance
metrics are already available.

The table below indicates the time taken in seconds to generate the convex
hull for a given number of points in a specified number of dimensions. The
final col (Cmd-line qconvex) is the time taken to generate the data using a
subprocess call to command line qconvex as a comparison for pyhull.

<table>
<tr>
<th>Number of points</th>
<th>Dim</th>
<th>scipy</th>
<th>pyhull</th>
<th>Cmd-line qconvex</th>
<tr>
<td>100</td><td>3</td>
<td>0.00237</td>
<td>0.00209</td>
<td>0.01354</td>
</tr>
<tr>
<td>100</td><td>4</td>
<td>0.00609</td>
<td>0.00333</td>
<td>0.01053</td>
</tr>
<tr>
<td>100</td><td>5</td>
<td>0.03125</td>
<td>0.00834</td>
<td>0.01743</td>
</tr>
<tr>
<td>100</td><td>6</td>
<td>0.16662</td>
<td>0.04627</td>
<td>0.05048</td>
</tr>
<tr>
<td>1000</td><td>3</td>
<td>0.02543</td>
<td>0.01166</td>
<td>0.01398</td>
</tr>
<tr>
<td>1000</td><td>4</td>
<td>0.15308</td>
<td>0.01438</td>
<td>0.01741</td>
</tr>
<tr>
<td>1000</td><td>5</td>
<td>1.04724</td>
<td>0.05105</td>
<td>0.05279</td>
</tr>
<tr>
<td>1000</td><td>6</td>
<td>7.45985</td>
<td>0.25104</td>
<td>0.29058</td>
</tr>
<tr>
<td>2000</td><td>3</td>
<td>0.05124</td>
<td>0.01968</td>
<td>0.02431</td>
</tr>
<tr>
<td>2000</td><td>4</td>
<td>0.32277</td>
<td>0.02326</td>
<td>0.02742</td>
</tr>
<tr>
<td>2000</td><td>5</td>
<td>2.38308</td>
<td>0.06664</td>
<td>0.06845</td>
</tr>
<tr>
<td>2000</td><td>6</td>
<td>20.64062</td>
<td>0.41188</td>
<td>0.42673</td>
</tr>
</table>

It is clear from the above table that even in its early alpha form,
pyhull outperforms scipy.spatial for large number of points in higher
dimensions. Also, pyhull is tested to be safe in terms of usage with Python
multiprocessing, unlike a subprocess call to Qhull.

Usage
=====

A C extension has been written, but it is generally recommended that you
use the high-level wrapper functions and classes instead.

Example usage of high-level functions:

    >>> from pyhull import qconvex, qdelaunay, qvoronoi
    >>>
    >>> pts = [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5], [0,0]]
    >>>
    >>> qconvex("i", pts)
    ['4\n', '0 2 \n', '1 0 \n', '2 3 \n', '3 1 \n']
    >>>
    >>> qdelaunay("i", pts)
    ['4\n', '2 4 0 \n', '4 1 0 \n', '3 4 2 \n', '4 3 1 \n']
    >>>
    >>> qvoronoi("o", pts)
    ['2\n', '5 5 1\n', '-10.101 -10.101 \n', '     0   -0.5 \n', '  -0.5      0 \n', '   0.5      0 \n', '     0    0.5 \n', '3 2 0 1\n', '3 4 0 2\n', '3 3 0 1\n', '3 4 0 3\n', '4 4 2 1 3\n']

The return values are simply a list of strings from the output.

For more useful analysis outputs, please use the high-level ConvexHull
and DelaunayTri classes in the convex_hull and delaunay modules. For example,

    >>> from pyhull.convex_hull import ConvexHull
    >>> hull = ConvexHull(pts)
    >>> hull.vertices
    [[0, 2], [1, 0], [2, 3], [3, 1]]
    >>> hull.points
    [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5], [0, 0]]
    >>>
    >>> from pyhull.delaunay import DelaunayTri
    >>> tri = DelaunayTri(pts)
    >>> tri.vertices
    [[2, 4, 0], [4, 1, 0], [3, 4, 2], [4, 3, 1]]
    >>> tri.points
    [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5], [0, 0]]
    >>>
