
use pyo3::prelude::*;

mod shape;
pub use shape::{Shape, Cuboid};

mod space;
pub use space::Space;

mod model;
pub use model::Model;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn deeper(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_class::<Shape>()?;
    m.add_class::<Cuboid>()?;
    m.add_class::<Space>()?;
    m.add_class::<Model>()?;
    Ok(())
}