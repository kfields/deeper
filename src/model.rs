use std::fmt::Debug;

use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;

#[pyclass]
pub struct Model {
    inner: i32,
}

#[pymethods]
impl Model {
    #[new]
    fn new(value: i32) -> Self {
        Model { inner: value }
    }
}
