pyhull
=======

pyhull is a port of Qhull (http://www.qhull.org/)  as a Python extension. It
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

pyqhull is still in the early stages of development, but some performance
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
dimensions.