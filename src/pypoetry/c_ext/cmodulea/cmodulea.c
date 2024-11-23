#include <Python.h>

// Function to print a message
static PyObject* print_hello_cmodulea(PyObject* self, PyObject* args) {
    printf("Hello to Python world from C world! I am CModule A\n");
    Py_RETURN_NONE;
}

// Method table for the module
static PyMethodDef CModuleMethods[] = {
    {"print_hello_cmodulea", print_hello_cmodulea, METH_NOARGS, "Prints a hello message from C"},
    {NULL, NULL, 0, NULL}  // Sentinel value
};

// Module definition
static struct PyModuleDef cmodulemodulea = {
    PyModuleDef_HEAD_INIT,
    "cmodulea",   // Module name
    "A simple example module",  // Module docstring
    -1,          // Size of per-interpreter state of the module
    CModuleMethods  // Method table
};

// Module initialization function
PyMODINIT_FUNC PyInit_cmodulea(void) {
    return PyModule_Create(&cmodulemodulea);
}
