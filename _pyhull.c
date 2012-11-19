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
char *tmp_input_file = "pyqconvex.in.tmp";
char *tmp_output_file = "pyqconvex.out.tmp";

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
  FILE *fp = fopen(tmp_input_file, "w");
  if (fp != NULL)
  {
        fputs(data, fp);

  }
  fclose(fp);

  FILE *stream = fopen(tmp_input_file, "r");
  FILE *output = fopen(tmp_output_file, "w");


  qh_init_A(stream, output, stderr, argc, argv);

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
  fclose(stream);
  fclose(output);
  FILE *outread = fopen(tmp_output_file, "r");
  char buffer[150], message[10000][150];
  int i=0;
  /*stores and prints the data from the string*/
  while(fgets(buffer,150,outread)){
    strcpy(message[i],buffer);
    i++;
  }
  fclose(outread);

  remove(tmp_input_file);
  remove(tmp_output_file);


  PyObject* pydata = PyList_New(i);
  int j;
  for (j = 0; j < i; j++)
  {
        PyList_SetItem(pydata, j, PyString_FromString(message[j]));
  }

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