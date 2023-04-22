import numpy as np
import pytest
import medmarch
from medmarch.mesh.compute_mesh import MedMarch


def test_init():
    vertices = np.array([[1, 2, 3], [4, 5, 6]])
    faces = np.array([[0, 1, 2], [1, 0, 2]])
    normals = np.array([[1, 0, 0], [0, 1, 0]])
    values = np.array([1.0, 2.0])

    med_march = MedMarch(vertices, faces, normals, values)

    assert np.array_equal(med_march.vertices, vertices)
    assert np.array_equal(med_march.faces, faces)
    assert np.array_equal(med_march.normals, normals)
    assert np.array_equal(med_march.values, values)


def test_compute_med_march_valid_input():
    volume = np.zeros((10, 10, 10))
    volume[3:7, 3:7, 3:7] = 1.0 # Create a cube of ones
    threshold = 0.5

    med_march = medmarch.compute(volume, threshold)

    assert isinstance(med_march, MedMarch)
    assert med_march.vertices.shape[1] == 3
    assert med_march.faces.shape[1] == 3
    assert med_march.normals.shape[1] == 3
    assert med_march.values.ndim == 1


def test_compute_med_march_invalid_volume():
    volume = np.zeros((10, 10))  # 2D array instead of 3D
    threshold = 0.5

    with pytest.raises(ValueError):
        medmarch.compute(volume, threshold)


def test_compute_med_march_invalid_threshold():
    volume = np.zeros((10, 10, 10))
    threshold = "invalid"  # Non-numeric value

    with pytest.raises(ValueError):
        medmarch.compute(volume, threshold)


def test_med_march_repr():
    vertices = np.array([[1, 2, 3], [4, 5, 6]])
    faces = np.array([[0, 1, 2], [1, 0, 2]])
    normals = np.array([[1, 0, 0], [0, 1, 0]])
    values = np.array([1.0, 2.0])

    med_march = MedMarch(vertices, faces, normals, values)
    repr_str = repr(med_march)

    assert repr_str == "MedMarch(vertices=(2, 3), faces=(2, 3), normals=(2, 3), values=(2,))"


def test_compute_med_march_error_handling():
    volume = np.zeros((10, 10, 10))
    threshold = 0.5

    with pytest.raises(RuntimeError):
        medmarch.compute(volume, threshold, method="invalid_method")
