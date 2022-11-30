use std::fmt::Debug;

use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyTuple};
use pyo3::Python;

use parry3d::bounding_volume::Aabb;
use parry3d::math::{Point, Real};

use crate::isometry::Isometry;

#[pyclass]
pub struct Body {
    center: Point<Real>,
    aabb: Aabb,
}

#[pymethods]
impl Body {
    #[new]
    fn new(_center: &PyTuple) -> Self {
        let x: Real = _center[0].extract::<Real>().unwrap();
        let y: Real = _center[1].extract::<Real>().unwrap();
        let z: Real = _center[2].extract::<Real>().unwrap();
        let center: Point<Real> = Point::new(x, y, z);
        Body {
            center,
            aabb: Aabb {
                mins: Point::origin(),
                maxs: Point::origin(),
            },
        }
    }

    /*#[getter]
    fn center(&self) -> PyResult<&PyTuple> {
        Ok(self.get_center(py))
    }*/

    /*#[getter]
    fn center(&self) -> PyResult<&PyTuple> {
        Python::with_gil(|py| -> PyResult<(&PyTuple)> {
            Ok(PyTuple::new(py, [self.center.x, self.center.y, self.center.z]))
        })    
    }*/

    /*#[getter]
    fn center<'py>(&'py self) -> PyResult<&PyTuple> {
        Python::with_gil(|py: Python<'py>| -> PyResult<&PyTuple> {
            Ok(PyTuple::new(py, [self.center.x, self.center.y, self.center.z]))
        })    
    }*/

    fn get_center<'py>(&'py self, py: Python<'py>) -> PyResult<&PyTuple> {
        let result: &PyTuple = PyTuple::new(py, [self.center.x, self.center.y, self.center.z]);
        Ok(result)
    }
}
