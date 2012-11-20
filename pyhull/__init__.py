__author__ = "Shyue Ping Ong"
__version__ = "1.0"


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
            info on supported options.
        points:
            Sequence of points as input to qhull command.
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
            An option string. See Qhull's qconvex help for info. Typically
            used options are:
            s - summary of results (default)
            i - vertices incident to each facet
            n - normals with offsets
            p - vertex coordinates (includes coplanar points if 'Qc')
        points:
            Sequence of points as input.

    Returns:
        Output as a list of strings.
    """
    return qhull_cmd("qconvex", options, points)


def qdelaunay(options, points):
    """
    Similar to qdelaunay command in command-line qhull.

    Args:
        options:
            An options string. See Qhull's qdelaunay help for info. Typically
            used options are:
            s - summary of results (default)
            i - vertices incident to each Delaunay region
            o - OFF format (shows the points lifted to a paraboloid)
        points:
            Sequence of points as input.

    Returns:
        Output as a list of strings.
    """
    return qhull_cmd("qdelaunay", options, points)


def qvoronoi(options, points):
    """
    Similar to qvoronoi command in command-line qhull.

    Args:
        option:
            An options string. See Qhull's qvoronoi help for info. Typically
            used options are:
            s - summary of results
            p - Voronoi vertices
            o - OFF file format (dim, Voronoi vertices, and Voronoi regions)
        points:
            Sequence of points as input.

    Returns:
        Output as a list of strings.
    """
    return qhull_cmd("qvoronoi", options, points)
