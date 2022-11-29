use std::fmt::Debug;

use pyo3::prelude::*;
use pyo3::exceptions::PyRuntimeError;
use pyo3::types::{PyDict, PyTuple};

use parry3d::math::{Real, Vector};
use parry3d::shape;

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
pub struct HalfSpace {
    pub inner: shape::HalfSpace,
}

#[pymethods]
impl HalfSpace {
    #[new]
    fn new(x: Real, y: Real, z: Real) -> (Self, Shape) {
        //TODO: Having trouble getting this right.  Using y_axis for now.
        //let normal: Unit<Vector3<Real>> = Unit::<Vector3<Real>>::new(x, y, z);
        let normal = Vector::<Real>::y_axis();
        (
            HalfSpace {
                inner: shape::HalfSpace { normal },
            },
            Shape::new(),
        )
    }
    fn __repr__(&self) -> String {
        let n = self.inner.normal;
        format!("HalfSpace(x={}, y={}, z={})", n.x, n.y, n.z)
    }
}

#[pyclass(extends=Shape, subclass)]
pub struct Cuboid {
    inner: shape::Cuboid,
}

#[pymethods]
impl Cuboid {
    #[new]
    fn new(x: Real, y: Real, z: Real) -> (Self, Shape) {
        let half_extents: Vector<Real> = Vector::new(x, y, z);
        (
            Cuboid {
                inner: shape::Cuboid { half_extents },
            },
            Shape::new(),
        )
    }
    fn __repr__(&self) -> String {
        let hf = self.inner.half_extents;
        format!("Cuboid(x={}, y={}, z={})", hf.x, hf.y, hf.z)
    }

    /*fn method2(self_: PyRef<'_, Self>) -> PyResult<usize> {
        let super_ = self_.as_ref(); // Get &BaseClass
        super_.method().map(|x| x * self_.val2)
    }*/
}
