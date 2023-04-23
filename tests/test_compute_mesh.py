import numpy as np
import pytest
from radvis.mesh import RadMesh, compute_marching_cubes


def test_init():
    vertices = np.array([[1, 2, 3], [4, 5, 6]])
    faces = np.array([[0, 1, 2], [1, 0, 2]])
    normals = np.array([[1, 0, 0], [0, 1, 0]])
    values = np.array([1.0, 2.0])

    rad_mesh = RadMesh(vertices, faces, normals, values)

    assert np.array_equal(rad_mesh.vertices, vertices)
    assert np.array_equal(rad_mesh.faces, faces)
    assert np.array_equal(rad_mesh.normals, normals)
    assert np.array_equal(rad_mesh.values, values)


def test_compute_rad_mesh_valid_input():
    volume = np.zeros((10, 10, 10))
    volume[3:7, 3:7, 3:7] = 1.0 # Create a cube of ones
    threshold = 0.5

    rad_mesh = compute_marching_cubes(volume, threshold)

    assert isinstance(rad_mesh, RadMesh)
    assert rad_mesh.vertices.shape[1] == 3
    assert rad_mesh.faces.shape[1] == 3
    assert rad_mesh.normals.shape[1] == 3
    assert rad_mesh.values.ndim == 1


def test_compute_rad_mesh_invalid_volume():
    volume = np.zeros((10, 10))  # 2D array instead of 3D
    threshold = 0.5

    with pytest.raises(ValueError):
        compute_marching_cubes(volume, threshold)


def test_compute_rad_mesh_invalid_threshold():
    volume = np.zeros((10, 10, 10))
    threshold = "invalid"  # Non-numeric value

    with pytest.raises(ValueError):
        compute_marching_cubes(volume, threshold)


def test_rad_mesh_repr():
    vertices = np.array([[1, 2, 3], [4, 5, 6]])
    faces = np.array([[0, 1, 2], [1, 0, 2]])
    normals = np.array([[1, 0, 0], [0, 1, 0]])
    values = np.array([1.0, 2.0])

    rad_mesh = RadMesh(vertices, faces, normals, values)
    repr_str = repr(rad_mesh)

    assert repr_str == "RadMesh(vertices=(2, 3), faces=(2, 3), normals=(2, 3), values=(2,))"


def test_compute_rad_mesh_error_handling():
    volume = np.zeros((10, 10, 10))
    threshold = 0.5

    with pytest.raises(RuntimeError):
        compute_marching_cubes(volume, threshold, method="invalid_method")
