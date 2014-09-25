"""
pyhull is a Python wrapper to Qhull (http://www.qhull.org/) for the
computation of the convex hull, Delaunay triangulation and Voronoi diagram.

Useful low-level functions are implemented for direct import in the base
package and can be called as pyhull.qconvex, pyhull.qdelauany, etc.
"""

__author__ = "Shyue Ping Ong"
__version__ = "1.5.3"
__date__ = "Sep 22 2014"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"


import pyhull._pyhull as hull


def qhull_cmd(cmd, options, points):
    """
    Generalized helper method to perform a qhull based command.

    Args:
        cmd:
            Command to perform. Supported commands are qconvex,
            qdelaunay and qvoronoi.
        options:
            Options to be provided for qhull command. See specific methods for
            info on supported options. Up to two options separated by spaces
            are supported.
        points:
            Sequence of points as input to qhull command.

     Returns:
        Output as a list of strings. E.g., ['4', '0 2', '1 0', '2 3 ', '3 1']
    """
    prep_str = [str(len(points[0])), str(len(points))]
    prep_str.extend([' '.join(map(repr, row)) for row in points])
    output = getattr(hull, cmd)(options, "\n".join(prep_str))
    return list(map(str.strip, output.strip().split("\n")))


def qconvex(options, points):
    """
    Similar to qconvex command in command-line qhull.

    Args:
        options:
            An option string. Up to two options separated by spaces
            are supported. See Qhull's qconvex help for info. Typically
            used options are:
            s - summary of results (default)
            i - vertices incident to each facet
            n - normals with offsets
            p - vertex coordinates (includes coplanar points if 'Qc')
        points:
            Sequence of points as input.

    Returns:
        Output as a list of strings. E.g., ['4', '0 2', '1 0', '2 3', '3 1']
    """
    return qhull_cmd("qconvex", options, points)


def qdelaunay(options, points):
    """
    Similar to qdelaunay command in command-line qhull.

    Args:
        options:
            An options string. Up to two options separated by spaces
            are supported. See Qhull's qdelaunay help for info. Typically
            used options are:
            s - summary of results (default)
            i - vertices incident to each Delaunay region
            o - OFF format (shows the points lifted to a paraboloid)
        points:
            Sequence of points as input.

    Returns:
        Output as a list of strings.
        E.g., ['4', '2 4 0', '4 1 0', '3 4 2', '4 3 1']
    """
    return qhull_cmd("qdelaunay", options, points)


def qvoronoi(options, points):
    """
    Similar to qvoronoi command in command-line qhull.

    Args:
        option:
            An options string. Up to two options separated by spaces
            are supported. See Qhull's qvoronoi help for info. Typically
            used options are:
            s - summary of results
            p - Voronoi vertices
            o - OFF file format (dim, Voronoi vertices, and Voronoi regions)
        points:
            Sequence of points as input.

    Returns:
        Output as a list of strings.
        E.g., ['2', '5 5 1', '-10.101 -10.101', '0   -0.5', '-0.5      0',
        '0.5      0', '0    0.5', '3 2 0 1', '3 4 0 2', '3 3 0 1',
        '3 4 0 3', '4 4 2 1 3']
    """
    return qhull_cmd("qvoronoi", options, points)


def qhalf(options, halfspaces, interior_point):
    """
    Similar to qvoronoi command in command-line qhull.

    Args:
        option:
            An options string. Up to two options separated by spaces
            are supported. See Qhull's qhalf help for info. Typically
            used options are:
            Fp
        halfspaces:
            List of Halfspaces as input.
        interior_point:
            An interior point (see qhalf documentation)

    Returns:
        Output as a list of strings.
        E.g., ['3', '4', '     1      1         0 ', '     1     -1      2 ',
        '    -1      1      2 ', '     1      1      2 ']
    """
    points = [list(h.normal) + [h.offset] for h in halfspaces]
    data = [[len(interior_point), 1]]
    data.append(map(repr, interior_point))
    data.append([len(points[0])])
    data.append([len(points)])
    data.extend([map(repr, row) for row in points])
    prep_str = [" ".join(map(str, line)) for line in data]
    output = getattr(hull, "qhalf")(options, "\n".join(prep_str))
    return list(map(str.strip, output.strip().split("\n")))
