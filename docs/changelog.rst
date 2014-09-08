Change log
==========

v1.4.6
------
1. Minor improvement to use the proper way to preserve float precision using
   repr.

v1.4.5
------
1. More precision fixes and bad code naming fixes.
   (Reported by Konrad Schneider).

v1.4.4
------
1. Fix the precision loss in conversion from floats to string in qhull_cmd
   (Reported by Konrad Schneider).

v1.4.3
-------
1. Add qhalf for pyhull (William Davidson Richards).

v1.3.6
------
1. Bug fix for non-Mac Linux systems.

v1.3.5
------
1. Minor update to remove stray debug print statement.

v1.3.3
------
1. Update to support any reasonable number of arguments in low level functions.

v1.3.2
------
1. Fix dangerous bug in fmemopen.c. String stream now works properly.

v1.3
----
1. Completely rewritten IO system using memstreams instead of open temp files.

v1.2.1
------
1. Minor additions of more properties and error checking.
2. Improve documentation.

v1.2
----
1. Improve robustness of underlying C extension.
2. Improve low level functions output.
3. Cleanup of docs.

v1.1
----
1. Minor update to support up to two arguments for low-level qhull calls.

v1.0
----
1. v1.0 release with all functionality tested and working.
