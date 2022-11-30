use pyo3::prelude::*;

use nalgebra::{Isometry3, Translation3, UnitQuaternion, Vector3};
use parry3d::math::{Real, Vector};

#[pyclass]
pub struct Isometry {
    pub inner: Isometry3<Real>,
}

#[pymethods]
impl Isometry {
    #[new]
    #[args(x="0.0", y="0.0", z="0.0", ax="0.0", ay="0.0", az="0.0")]
    fn new(x: Real, y: Real, z: Real, ax: Real, ay: Real, az: Real) -> Self {
        Isometry {
            inner: Isometry3::new(Vector3::new(x, y, z), Vector3::new(ax, ay, az))
        }
    }

    fn __repr__(&self) -> String {
        self.inner.to_string()
    }
}
