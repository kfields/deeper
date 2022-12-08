use pyo3::prelude::*;

use parry3d::bounding_volume;
use parry3d::math::{Point, Real};

#[pyclass]
pub struct Aabb {
    pub inner: bounding_volume::Aabb,
}

#[pymethods]
impl Aabb {
    #[new]
    #[args(minx = "0.0", miny = "0.0", minz = "0.0", maxx = "0.0", maxy = "0.0", maxz = "0.0")]
    fn new(minx: Real, miny: Real, minz: Real, maxx: Real, maxy: Real, maxz: Real) -> Self {
        Aabb {
            inner: bounding_volume::Aabb {
                mins: Point::new(minx, miny, minz),
                maxs: Point::new(maxx, maxy, maxz),
            },
        }
    }

    fn __repr__(&self) -> String {
        let mins = self.inner.mins;
        let maxs = self.inner.maxs;
        format!(
            "Aabb(minx={}, miny={}, minz={}, maxx={}, maxy={}, maxz={})",
            mins.x, mins.y, mins.z, maxs.x, maxs.y, maxs.z
        )
    }

    #[getter]
    fn minx(&self) -> Real {
        self.inner.mins.x
    }

    #[getter]
    fn miny(&self) -> Real {
        self.inner.mins.y
    }

    #[getter]
    fn minz(&self) -> Real {
        self.inner.mins.z
    }

    #[getter]
    fn maxx(&self) -> Real {
        self.inner.maxs.x
    }

    #[getter]
    fn maxy(&self) -> Real {
        self.inner.maxs.y
    }

    #[getter]
    fn maxz(&self) -> Real {
        self.inner.maxs.z
    }

}
