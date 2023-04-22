import numpy as np
import pytest
from resview.mesh.compute_mesh import ResMesh


def test_init():
    vertices = np.array([[1, 2, 3], [4, 5, 6]])
    faces = np.array([[0, 1, 2], [1, 0, 2]])
    normals = np.array([[1, 0, 0], [0, 1, 0]])
    values = np.array([1.0, 2.0])

    res_mesh = ResMesh(vertices, faces, normals, values)

    assert np.array_equal(res_mesh.vertices, vertices)
    assert np.array_equal(res_mesh.faces, faces)
    assert np.array_equal(res_mesh.normals, normals)
    assert np.array_equal(res_mesh.values, values)


def test_compute_res_mesh_valid_input():
    volume = np.zeros((10, 10, 10))
    volume[3:7, 3:7, 3:7] = 1.0 # Create a cube of ones
    threshold = 0.5

    res_mesh = ResMesh.compute(volume, threshold)

    assert isinstance(res_mesh, ResMesh)
    assert res_mesh.vertices.shape[1] == 3
    assert res_mesh.faces.shape[1] == 3
    assert res_mesh.normals.shape[1] == 3
    assert res_mesh.values.ndim == 1


def test_compute_res_mesh_invalid_volume():
    volume = np.zeros((10, 10))  # 2D array instead of 3D
    threshold = 0.5

    with pytest.raises(ValueError):
        ResMesh.compute(volume, threshold)


def test_compute_res_mesh_invalid_threshold():
    volume = np.zeros((10, 10, 10))
    threshold = "invalid"  # Non-numeric value

    with pytest.raises(ValueError):
        ResMesh.compute(volume, threshold)


def test_res_mesh_repr():
    vertices = np.array([[1, 2, 3], [4, 5, 6]])
    faces = np.array([[0, 1, 2], [1, 0, 2]])
    normals = np.array([[1, 0, 0], [0, 1, 0]])
    values = np.array([1.0, 2.0])

    res_mesh = ResMesh(vertices, faces, normals, values)
    repr_str = repr(res_mesh)

    assert repr_str == "ResMesh(vertices=(2, 3), faces=(2, 3), normals=(2, 3), values=(2,))"


def test_compute_res_mesh_error_handling():
    volume = np.zeros((10, 10, 10))
    threshold = 0.5

    with pytest.raises(RuntimeError):
        ResMesh.compute(volume, threshold, method="invalid_method")
