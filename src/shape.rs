use std::fmt::Debug;

use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyTuple};

use parry3d::math::{Real, Vector};
use parry3d::query::RayCast;
use parry3d::shape;

use crate::isometry::Isometry;
use crate::query::Ray;
use crate::bounding_volume::Aabb;

pub trait ShapeTrait {
    fn get_inner(&self) -> &dyn shape::Shape;
}

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

impl ShapeTrait for HalfSpace {
    fn get_inner(&self) -> &dyn shape::Shape {
        return &self.inner;
    }
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

    fn cast_ray(&self, position: &Isometry, ray: &Ray, py: Python) -> PyResult<PyObject> {
        let intersection =
            self.inner
                .cast_ray_and_get_normal(&position.inner, &ray.inner, std::f32::MAX, true);

        if let Some(intersection) = intersection {
            let point = ray.inner.origin + ray.inner.dir * intersection.toi;
            let result = PyTuple::new(py, [point.x, point.y, point.z]);
            Ok(result.into())
        } else {
            Ok(py.None())
        }
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
        let half_extents: Vector<Real> = Vector::new(x*0.5, y*0.5, z*0.5);
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
    fn aabb(&self, pos: &Isometry) -> Aabb {
        let aabb = self.inner.aabb(&pos.inner);
        Aabb { inner: aabb }
    }
    //TODO:  We're repeating ourselves
    fn cast_ray(&self, position: &Isometry, ray: &Ray, py: Python) -> PyResult<PyObject> {
        let intersection =
            self.inner
                .cast_ray_and_get_normal(&position.inner, &ray.inner, std::f32::MAX, true);

        if let Some(intersection) = intersection {
            let point = ray.inner.origin + ray.inner.dir * intersection.toi;
            let result = PyTuple::new(py, [point.x, point.y, point.z]);
            Ok(result.into())
        } else {
            Ok(py.None())
        }
    }
}
