use edi::*;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;

use pythonize::{depythonize, pythonize};
use std::fmt;

struct PyEdiDocument<'a>(EdiDocument<'a>);

impl<'a, 'b> IntoPy<PyObject> for PyEdiDocument<'a> {
    fn into_py(self, py: Python<'_>) -> PyObject {
        pythonize(py, &self.0).unwrap()
    }
}

#[derive(Debug, Clone)]
struct PyEdiParseError {
    message: String,
}

impl fmt::Display for PyEdiParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let message = self.to_string();
        write!(f, "{message}")
    }
}

impl std::error::Error for PyEdiParseError {}

impl std::convert::From<PyEdiParseError> for PyErr {
    fn from(err: PyEdiParseError) -> PyErr {
        PyValueError::new_err(err.message)
    }
}

impl std::convert::From<EdiParseError> for PyEdiParseError {
    fn from(other: EdiParseError) -> Self {
        Self {
            message: other.to_string(),
        }
    }
}

#[pyfunction]
fn rs_loose_parse(path: &str) -> Result<PyObject, PyEdiParseError> {
    let contents = std::fs::read_to_string(path).unwrap();
    let doc = loose_parse(&contents)?;

    Python::with_gil(|py| {
        let doc = pythonize(py, &doc).unwrap();
        Ok(doc)
    })
}

#[pyfunction]
fn rs_parse(path: &str) -> Result<PyObject, PyEdiParseError> {
    let contents = std::fs::read_to_string(path).unwrap();
    Python::with_gil(|py| {
        let doc = parse(&contents)?;
        let doc = pythonize(py, &doc).unwrap();
        Ok(doc)
    })
}

#[pyfunction]
fn rs_to_x12_string(edi_obj: &PyDict) -> String {
    // deserialize here requires fork of edi
    // where Transaction.transaction_name is Cow<'a, str> instead of &'b str
    // see https://users.rust-lang.org/t/solved-serde-deserialize-str-containig-special-chars/27218
    let doc: EdiDocument = depythonize(edi_obj).unwrap();
    doc.to_x12_string()
}

/// A Python module implemented in Rust.
#[pymodule]
fn edio3(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rs_parse, m)?)?;
    m.add_function(wrap_pyfunction!(rs_loose_parse, m)?)?;
    m.add_function(wrap_pyfunction!(rs_to_x12_string, m)?)?;
    Ok(())
}
