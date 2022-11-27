use std::fmt::Debug;

use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyTuple};

use parry3d::math::{Real, Vector};
use parry3d::shape::Cuboid as ParryCuboid;

#[pyclass(subclass)]
pub struct Shape {}

#[pymethods]
impl Shape {
    #[new]
    fn new() -> Self {
        Shape {}
    }
}

#[pyclass(extends=Shape, subclass)]
pub struct Cuboid {
    inner: ParryCuboid,
}

#[pymethods]
impl Cuboid {
    #[new]
    fn new(_half_extents: &PyTuple) -> (Self, Shape) {
        let arg1: Real = _half_extents[0].extract::<Real>().unwrap();
        let arg2: Real = _half_extents[1].extract::<Real>().unwrap();
        let arg3: Real = _half_extents[2].extract::<Real>().unwrap();
        let half_extents: Vector<Real> = Vector::new(arg1, arg2, arg3);
        (
            Cuboid {
                inner: ParryCuboid { half_extents },
            },
            Shape::new(),
        )
    }

    /*fn method2(self_: PyRef<'_, Self>) -> PyResult<usize> {
        let super_ = self_.as_ref(); // Get &BaseClass
        super_.method().map(|x| x * self_.val2)
    }*/
}
