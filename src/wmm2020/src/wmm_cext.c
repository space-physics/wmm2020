#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "wmm_point_sub.h"


static PyObject *
wmm_cext_wmmsub(PyObject *self, PyObject *args, PyObject *kwds)
{
    char* wmm_filename = "WMM.COF";
    double geolatitude;
    double geolongitude;
    double HeightAboveEllipsoid;
    double yeardecimal;
    double x;
    double y;
    double z;
    double f;
    double decl;
    double incl;
    int ret;


    // Parse the arguments
    static char *kwlist[] = {"geolatitude", "geolongitude", "HeightAboveEllipsoid", "yeardecimal", "wmm_filename", NULL};
    if (! PyArg_ParseTupleAndKeywords(args, kwds, "dddd|z", kwlist,
                                      &geolatitude, &geolongitude, &HeightAboveEllipsoid, &yeardecimal, &wmm_filename))
        return NULL;

    ret = wmmsub_f(geolatitude, geolongitude, HeightAboveEllipsoid, yeardecimal,
                   &x, &y, &z, &f, &decl, &incl, wmm_filename);

    if (ret == 0){
        return Py_BuildValue("(d, d, d, d, d, d)", x, y, z, f, decl, incl);
    }

    // Raise a error
    PyErr_SetString(PyExc_FileNotFoundError, "WMM.COF not found.");
    return NULL;
}


static PyMethodDef wmm_cext_module_methods[] = {
    {"wmmsub", (PyCFunction)wmm_cext_wmmsub, METH_VARARGS | METH_KEYWORDS,
     "WMM Point Calculation Program.\n"
     "\n"
     "The Geomagnetism Library is used to make a command prompt program. The program prompts\n"
     "the user to enter a location, performs the computations and prints the results to the\n"
     "standard output. The program expects the files GeomagnetismLibrary.c, GeomagnetismHeader.h,\n"
     "WMM.COF and EGM9615.h to be in the same directory.\n"
     "\n"
     "Args:\n"
     "    geolatitude (float): latitude.\n"
     "    geolongitude (float): longitude.\n"
     "    HeightAboveEllipsoid (float): .\n"
     "    yeardecimal (float): .\n"
     "    wmm_filename (str)['WMM.COF']: Filename that points to the WMM.COF.\n"
     "\n"
     "Returns:\n"
     "    x (float): .\n"
     "    y (float): .\n"
     "    z (float): .\n"
     "    f (float): .\n"
     "    decl (float): .\n"
     "    incl (float): .\n"},

    {NULL}  /* Sentinel */
};


// Note: "wmm_cext" is the compiled name. It will compile to "wmm_cext.pyd"
#if PY_MAJOR_VERSION >= 3
// Python 3.x

static struct PyModuleDef c2module = {
    PyModuleDef_HEAD_INIT,
    "wmm_cext",
    "WMM Python C Extension.",
    -1,
    wmm_cext_module_methods, NULL, NULL, NULL, NULL
};


PyMODINIT_FUNC
PyInit_wmm_cext(void)
{
    PyObject* m;

    m = PyModule_Create(&c2module);
    if (m == NULL) return NULL;

    return m;
}

#else
// Python 2.7
#define INITERROR return


PyMODINIT_FUNC
init_wmm_cext(void)
{
    PyObject* m;

    m = Py_InitModule("wmm_ext", wmm_ext_module_methods);
    if (m == NULL) return;
}

#endif
