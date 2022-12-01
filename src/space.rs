use std::fmt::Debug;

//use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::{PyTuple, PyList};
use pyo3::Python;
use parry3d::bounding_volume::Aabb;
use parry3d::math::{Point, Real};

use crate::isometry::Isometry;

#[pyclass]
pub struct Space {
    /*#[pyo3(get)]
    parent: Py<Space>,*/
    #[pyo3(get)]
    children: Py<PyList>,
    #[pyo3(get)]
    isometry: Py<Isometry>,
    aabb: Aabb,
}

#[pymethods]
impl Space {
    #[new]
    //#[args(position="Isometry()")]
    fn new<'py>(isometry: Py<Isometry>, py: Python<'py>) -> Self {
        let list = PyList::empty(py).into_py(py);
        Space {
            isometry,
            children: list,
            aabb: Aabb {
                mins: Point::origin(),
                maxs: Point::origin(),
            },
        }
    }
    /*#[args(parent="None")]
    fn new<'py>(parent: Py<Space>, py: Python<'py>) -> Self {
        let list = PyList::empty(py).into_py(py);
        Space {
            parent,
            isometry: Isometry::new(),
            children: list,
            aabb: Aabb {
                mins: Point::origin(),
                maxs: Point::origin(),
            },
        }
    }*/

    /*#[getter]
    fn center(& self) -> PyResult<&PyTuple> {
        Python::with_gil(|py| -> PyResult<&PyTuple> {
            //let isometry: &Isometry = self.isometry.extract(py).unwrap();
            //let isometry = &self.isometry.extract::<Isometry>(py).unwrap();
            let isometry = self.isometry.as_ref(py).borrow().inner;
            //let x: Real = _center[0].extract::<Real>().unwrap();
            let center = isometry.translation; 
            Ok(PyTuple::new(py, [center.x, center.y, center.z]))
        })    
    }*/

    #[getter]
    fn center(& self) -> Py<PyTuple> {
        Python::with_gil(|py| -> Py<PyTuple> {
            //let isometry: &Isometry = self.isometry.extract(py).unwrap();
            //let isometry = &self.isometry.extract::<Isometry>(py).unwrap();
            let isometry = self.isometry.as_ref(py).borrow().inner;
            //let x: Real = _center[0].extract::<Real>().unwrap();
            let center = isometry.translation; 
            PyTuple::new(py, [center.x, center.y, center.z]).into_py(py)
        })    
    }

    fn add_child<'py>(&self, space: Py<Space>, py: Python<'py>) {
        let list: &PyList = self.children.as_ref(py);
        list.append(space);
    }
}
