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

/*-<a                             href="../libqhull/qh-qhull.htm#TOC"
  >-------------------------------</a><a name="prompt">-</a>

  qh_prompt
    long prompt for qconvex

  notes:
    restricted version of libqhull.c

  see:
    concise prompt below
*/

/* duplicated in qconvex.htm */
char hidden_options[]=" d v H Qbb Qf Qg Qm Qr Qu Qv Qx Qz TR E V Fp Gt Q0 Q1 Q2 Q3 Q4 Q5 Q6 Q7 Q8 Q9 ";
char * tmp_in_prefix = "pyqconvex.in";
char * tmp_out_prefix = "pyqconvex.out";

static PyObject* qconvex(PyObject *self, PyObject *args) {
  int argc;
  char *argv[2];
  const char *argvar;
  const char *data;
  int curlong, totlong; /* used !qh_NOmem */
  int exitcode, numpoints, dim;
  coordT *points;
  boolT ismalloc;
  if (!PyArg_ParseTuple(args, "ss", &argvar, &data))
      return NULL;
  argc=2;
  argv[0] = argvar;
  argv[1] = argvar;

  char *tmp_input_file = tempnam(NULL, tmp_in_prefix);
  char *tmp_output_file = tempnam(NULL, tmp_in_prefix);

  /* Because qhull uses stdin and stdout streams for io, we need to create
  FILE* stream to simulate these io streams. Suggestions on a better
  cross-platform way to implement a string stream equivalent are welcome.*/
  FILE *fin = fopen(tmp_input_file, "w");
  if (fin != NULL)
  {
        fputs(data, fin);
  }
  else
  {
     return NULL;
  }
  fclose(fin);

  /* Now do the usual qhull code (modified from qconvex.c). */
  fin = fopen(tmp_input_file, "r");
  FILE *fout = fopen(tmp_output_file, "w");
  if ((fin != NULL) && (fout != NULL))
  {

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
      fclose(fin);
      fclose(fout);
  }
  else
  {
       return NULL;
  }

  /* We need to know the number of lines in the file to allocate the PyList
  object */
  PyObject* pydata;
  fout = fopen(tmp_output_file, "r");
  if (fout != NULL)
  {
      int count = 0;
      int MAX_BUF_SIZE = 100;
      char buffer[MAX_BUF_SIZE];
      while(fgets(buffer, MAX_BUF_SIZE, fout)){
          count++;
      }
      fseek(fout, 0, SEEK_SET);
      int i = 0;

      pydata = PyList_New(count);
      /*stores and prints the data from the string*/
      while(fgets(buffer,MAX_BUF_SIZE, fout)){
        PyList_SetItem(pydata, i, PyString_FromString(buffer));
        i++;
      }
      fclose(fout);
  }
  else{
    return NULL;
  }

  remove(tmp_input_file);
  remove(tmp_output_file);
  return pydata;
}


static PyMethodDef QhullMethods[] = {
    {"qconvex",  qconvex, METH_VARARGS, "qconvex"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


void init_pyhull(void)
{
    (void) Py_InitModule("_pyhull", QhullMethods);
}