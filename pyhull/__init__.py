"""
pyhull is a Python wrapper to Qhull (http://www.qhull.org/) for the
computation of the convex hull, Delaunay triangulation and Voronoi diagram.

Useful low-level functions are implemented for direct import in the base
package and can be called as pyhull.qconvex, pyhull.qdelauany, etc.
"""

__author__ = "Shyue Ping Ong"
__version__ = "1.3"
__date__ = "Nov 20 2012"
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
    prep_str.extend([' '.join([str(i) for i in row]) for row in points])
    toks = options.split()
    if len(toks) == 1:
        return getattr(hull, cmd)(options, "\n".join(prep_str))
    else:
        return getattr(hull, cmd)(toks[0], toks[1], "\n".join(prep_str))


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
    return [l.strip() for l in qhull_cmd("qconvex", options, points)]


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
    return [l.strip() for l in qhull_cmd("qdelaunay", options, points)]


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
    return [l.strip() for l in qhull_cmd("qvoronoi", options, points)]
