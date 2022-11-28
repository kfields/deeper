use std::fmt::Debug;

//use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::PyList;
//use pyo3::Python;

use crate::body::Body;

#[pyclass]
pub struct Space {
    #[pyo3(get)]
    bodies: Py<PyList>,
}

#[pymethods]
impl Space {
    #[new]
    fn new<'py>(py: Python<'py>) -> Self {
        let list = PyList::empty(py).into_py(py);
        Space { bodies: list }
    }

    fn add_body<'py>(&self, body: Py<Body>, py: Python<'py>) {
        let list: &PyList = self.bodies.as_ref(py);
        list.append(body);
    }
}
