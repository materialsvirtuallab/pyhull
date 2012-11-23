#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include "libqhull.h"
#include "mem.h"
#include "qset.h"

#if __MWERKS__ && __POWERPC__
#include <SIOUX.h>
#include <Files.h>
#include <console.h>
#include <Desk.h>

#elif __cplusplus
extern "C" {
  int isatty(int);
}

#elif _MSC_VER
#include <io.h>
#define isatty _isatty
int _isatty(int);

#else
int isatty(int);  /* returns 1 if stdin is a tty
                   if "Undefined symbol" this can be deleted along with call in main() */
#endif

#ifdef __APPLE__
#include "fmemopen.h"
#include "open_memstream.h"
#endif

/* duplicated in qconvex.htm */
char hidden_options[]=" d v H Qbb Qf Qg Qm Qr Qu Qv Qx Qz TR E V Fp Gt Q0 Q1 Q2 Q3 Q4 Q5 Q6 Q7 Q8 Q9 ";

static PyObject* qconvex(PyObject *self, PyObject *args) {

  const char *arg1;
  const char *arg2 = "";
  const char *data = "";
  int curlong, totlong; /* used !qh_NOmem */
  int exitcode, numpoints, dim;
  coordT *points;
  boolT ismalloc;
  if (!PyArg_ParseTuple(args, "s|ss", &arg1, &arg2, &data))
      return NULL;
  char *argv[3];
  int argc = 2;
  argv[0] = arg1;
  argv[1] = arg1;
  if (strcmp(data, "") != 0)
  {
    argv[2] = arg2;
    argc += 1;
  }
  else{
    data = arg2;
  }

  char *bp;
  size_t size;

  /* Because qhull uses stdin and stdout streams for io, we need to create
  FILE* stream to simulate these io streams.*/
  FILE* fin = fmemopen(data, strlen(data), "r");
  FILE* fout = open_memstream(&bp, &size);

  PyObject* pydata;
  if ((fin != NULL) && (fout != NULL))
  {
     fseek(fin, 0, SEEK_SET);
     /* Now do the usual qhull code (modified from qconvex.c). */
     qh_init_A(fin, fout, stderr, argc, argv);

     exitcode= setjmp(qh errexit);
     if (!exitcode) {
        qh_checkflags(qh qhull_command, hidden_options);
        qh_initflags(qh qhull_command);
        points= qh_readpoints(&numpoints, &dim, &ismalloc);
        if (dim >= 5) {
           qh_option("Qxact_merge", NULL, NULL);
           qh MERGEexact= True;
        }
        qh_init_B(points, numpoints, dim, ismalloc);
        qh_qhull();
        qh_check_output();
        qh_produce_output();
        if (qh VERIFYoutput && !qh FORCEoutput && !qh STOPpoint && !qh STOPcone)
           qh_check_points();
        exitcode= qh_ERRnone;
     }
     qh NOerrexit= True;  /* no more setjmp */
     #ifdef qh_NOmem
        qh_freeqhull( True);
     #else
        qh_freeqhull( False);
        qh_memfreeshort(&curlong, &totlong);
        if (curlong || totlong)
           fprintf(stderr, "qhull internal warning (main): did not free %d bytes of long memory(%d pieces)\n",
           totlong, curlong);
     #endif
     fclose(fin);
     fclose(fout);
     return Py_BuildValue("s", bp);
  }
  else
  {
     return NULL;
  }
}

static PyObject* qdelaunay(PyObject *self, PyObject *args) {
  const char *arg1;
    const char *arg2 = "";
    const char *data = "";
    int curlong, totlong; /* used !qh_NOmem */
    int exitcode, numpoints, dim;
    coordT *points;
    boolT ismalloc;
    if (!PyArg_ParseTuple(args, "s|ss", &arg1, &arg2, &data))
        return NULL;
    char *argv[3];
    int argc = 2;
    argv[0] = arg1;
    argv[1] = arg1;
    if (strcmp(data, "") != 0)
    {
      argv[2] = arg2;
      argc += 1;
    }
    else{
      data = arg2;
    }


  char *bp;
  size_t size;

  /* Because qhull uses stdin and stdout streams for io, we need to create
  FILE* stream to simulate these io streams.*/
  FILE* fin = fmemopen(data, strlen(data), "r");
  FILE* fout = open_memstream(&bp, &size);

  PyObject* pydata;
  if ((fin != NULL) && (fout != NULL))
  {
     fseek(fin, 0, SEEK_SET);
     /* Now do the usual qhull code (modified from qconvex.c). */
     qh_init_A(fin, fout, stderr, argc, argv);  /* sets qh qhull_command */
     exitcode= setjmp(qh errexit); /* simple statement for CRAY J916 */
     if (!exitcode) {
        qh_option("delaunay  Qbbound-last", NULL, NULL);
        qh DELAUNAY= True;     /* 'd'   */
        qh SCALElast= True;    /* 'Qbb' */
        qh KEEPcoplanar= True; /* 'Qc', to keep coplanars in 'p' */
        qh_checkflags(qh qhull_command, hidden_options);
        qh_initflags(qh qhull_command);
        points= qh_readpoints(&numpoints, &dim, &ismalloc);
        if (dim >= 5) {
           qh_option("Qxact_merge", NULL, NULL);
           qh MERGEexact= True; /* 'Qx' always */
        }
        qh_init_B(points, numpoints, dim, ismalloc);
        qh_qhull();
        qh_check_output();
        qh_produce_output();
        if (qh VERIFYoutput && !qh FORCEoutput && !qh STOPpoint && !qh STOPcone)
           qh_check_points();
        exitcode= qh_ERRnone;
     }
     qh NOerrexit= True;  /* no more setjmp */
     #ifdef qh_NOmem
       qh_freeqhull( True);
     #else
       qh_freeqhull( False);
       qh_memfreeshort(&curlong, &totlong);
       if (curlong || totlong)
         fprintf(stderr, "qhull internal warning (main): did not free %d bytes of long memory(%d pieces)\n",
            totlong, curlong);
     #endif

     fclose(fin);
     fclose(fout);
     return Py_BuildValue("s", bp);
  }
  else
  {
     return NULL;
  }
}


static PyObject* qvoronoi(PyObject *self, PyObject *args) {
  const char *arg1;
    const char *arg2 = "";
    const char *data = "";
    int curlong, totlong; /* used !qh_NOmem */
    int exitcode, numpoints, dim;
    coordT *points;
    boolT ismalloc;
    if (!PyArg_ParseTuple(args, "s|ss", &arg1, &arg2, &data))
        return NULL;
    char *argv[3];
    int argc = 2;
    argv[0] = arg1;
    argv[1] = arg1;
    if (strcmp(data, "") != 0)
    {
      argv[2] = arg2;
      argc += 1;
    }
    else{
      data = arg2;
    }

  char *bp;
  size_t size;

  /* Because qhull uses stdin and stdout streams for io, we need to create
  FILE* stream to simulate these io streams.*/
  FILE* fin = fmemopen(data, strlen(data), "r");
  FILE* fout = open_memstream(&bp, &size);

  PyObject* pydata;
  if ((fin != NULL) && (fout != NULL))
  {
     fseek(fin, 0, SEEK_SET);
     /* Now do the usual qhull code (modified from qconvex.c). */
     qh_init_A(fin, fout, stderr, argc, argv);  /* sets qh qhull_command */
     exitcode= setjmp(qh errexit); /* simple statement for CRAY J916 */
       if (!exitcode) {
         qh_option("voronoi  _bbound-last  _coplanar-keep", NULL, NULL);
         qh DELAUNAY= True;     /* 'v'   */
         qh VORONOI= True;
         qh SCALElast= True;    /* 'Qbb' */
         qh_checkflags(qh qhull_command, hidden_options);
         qh_initflags(qh qhull_command);
         points= qh_readpoints(&numpoints, &dim, &ismalloc);
         if (dim >= 5) {
           qh_option("_merge-exact", NULL, NULL);
           qh MERGEexact= True; /* 'Qx' always */
         }
         qh_init_B(points, numpoints, dim, ismalloc);
         qh_qhull();
         qh_check_output();
         qh_produce_output();
         if (qh VERIFYoutput && !qh FORCEoutput && !qh STOPpoint && !qh STOPcone)
           qh_check_points();
         exitcode= qh_ERRnone;
       }
       qh NOerrexit= True;  /* no more setjmp */
     #ifdef qh_NOmem
       qh_freeqhull( True);
     #else
       qh_freeqhull( False);
       qh_memfreeshort(&curlong, &totlong);
       if (curlong || totlong)
         fprintf(stderr, "qhull internal warning (main): did not free %d bytes of long memory(%d pieces)\n",
            totlong, curlong);
     #endif
     fclose(fin);
     fclose(fout);
     /* We need to know the number of lines in the file to allocate the PyList
     object */

     return Py_BuildValue("s", bp);
  }
  else
  {
     return NULL;
  }
}


static PyMethodDef QhullMethods[] = {
    {"qconvex", qconvex, METH_VARARGS, "qconvex"},
    {"qdelaunay", qdelaunay, METH_VARARGS, "qdelaunay"},
    {"qvoronoi", qvoronoi, METH_VARARGS, "qvoronoi"},
    {NULL, NULL, 0, NULL}
};


void init_pyhull(void)
{
    (void) Py_InitModule("_pyhull", QhullMethods);
}