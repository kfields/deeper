use std::fmt::Debug;

//use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::PyList;
use pyo3::Python;

use crate::isometry::Isometry;

#[pyclass]
pub struct Space {
    #[pyo3(get)]
    position: Py<Isometry>,
    #[pyo3(get)]
    children: Py<PyList>,
}

#[pymethods]
impl Space {
    #[new]
    //#[args(position="Isometry()")]
    fn new<'py>(position: Py<Isometry>, py: Python<'py>) -> Self {
        let list = PyList::empty(py).into_py(py);
        Space {
            position,
            children: list,
        }
    }

    fn add_child<'py>(&self, space: Py<Space>, py: Python<'py>) {
        let list: &PyList = self.children.as_ref(py);
        list.append(space);
    }
}
