use std::fmt::Debug;

use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyTuple};

use nalgebra::{Unit, Vector3};

use parry3d::math::{Point, Real, Vector};
use parry3d::query;
use parry3d::shape::FeatureId;

#[pyclass]
pub struct Ray {
    pub inner: query::Ray,
}

#[pymethods]
impl Ray {
    #[new]
    fn new(x: Real, y: Real, z: Real, dx: Real, dy: Real, dz: Real) -> Self {
        let origin: Point<Real> = Point::new(x, y, z);
        let dir: Vector<Real> = Vector::new(dx, dy, dz);
        Ray {
            inner: query::Ray { origin, dir },
        }
    }
    #[getter]
    fn origin(& self) -> Py<PyTuple> {
        Python::with_gil(|py| -> Py<PyTuple> {
            let origin = self.inner.origin;
            PyTuple::new(py, [origin.x, origin.y, origin.z]).into_py(py)
        })    
    }
    fn __repr__(&self) -> String {
        let o = self.inner.origin;
        let d = self.inner.dir;
        format!(
            "Ray(x={}, y={}, z={}, dx={}, dy={}, dz={})",
            o.x, o.y, o.z, d.x, d.y, d.z
        )
    }
}

#[pyclass]
pub struct RayIntersection {
    pub inner: query::RayIntersection,
}

#[pymethods]
impl RayIntersection {
    /*#[staticmethod]
    fn static_method(param1: i32, param2: &str) -> PyResult<i32> {
        Ok(10)
    }*/
    /*fn create(_inner: query::RayIntersection) -> RayIntersection {
        RayIntersection { inner: _inner }
    }*/
    #[new]
    fn new(toi: Real, x: Real, y: Real, z: Real) -> Self {
        let normal: Vector<Real> = Vector::new(x, y, z);
        RayIntersection {
            inner: query::RayIntersection { toi, normal, feature: FeatureId::Unknown },
        }
    }
    /*fn __repr__(&self) -> String {
        let o = self.inner.origin;
        let d = self.inner.dir;
        format!(
            "Ray(x={}, y={}, z={}, dx={}, dy={}, dz={})",
            o.x, o.y, o.z, d.x, d.y, d.z
        )
    }*/
}
