use std::fmt::Debug;

use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;

#[pyclass]
pub struct Space {
    inner: i32,
}

#[pymethods]
impl Space {
    #[new]
    fn new(value: i32) -> Self {
        Space { inner: value }
    }
}
