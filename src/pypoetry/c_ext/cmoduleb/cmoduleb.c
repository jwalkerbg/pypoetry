#include <Python.h>

// Function to print a message
static PyObject* print_hello_cmoduleb(PyObject* self, PyObject* args) {
    printf("Hello to Python world from C world! I am CModule B!\n");
    Py_RETURN_NONE;
}

// Method table for the module
static PyMethodDef CmodulebMethods[] = {
    {"print_hello_cmoduleb", print_hello_cmoduleb, METH_NOARGS, "Prints a hello message from C"},
    {NULL, NULL, 0, NULL}  // Sentinel value
};

// Module definition
static struct PyModuleDef cmodulecmoduleb = {
    PyModuleDef_HEAD_INIT,
    "cmoduleb",   // Module name
    "A simple example module",  // Module docstring
    -1,          // Size of per-interpreter state of the module
    CmodulebMethods  // Method table
};

// Module initialization function
PyMODINIT_FUNC PyInit_cmoduleb(void) {
    return PyModule_Create(&cmodulecmoduleb);
}
