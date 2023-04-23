import os
import tempfile
import numpy as np
import re
from radvis.mesh import RadMesh
from radvis.io.save import save_radmesh


def create_test_radmesh():
    vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    faces = np.array([[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]])
    normals = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 1, 1]])
    values = np.array([0.0, 0.5, 1.0, 1.5])

    return RadMesh(vertices, faces, normals, values)


def test_save_radmesh_supported_formats():
    radmesh = create_test_radmesh()
    supported_formats = ["stl", "obj", "ply", "vtk"]

    for file_format in supported_formats:
        fd, temp_file = tempfile.mkstemp(suffix=f".{file_format}")
        os.close(fd)
        try:
            save_radmesh(radmesh, temp_file, file_format)
            assert os.path.exists(temp_file)
        finally:
            os.remove(temp_file)


def test_save_radmesh_unsupported_format():
    radmesh = create_test_radmesh()

    fd, temp_file = tempfile.mkstemp(suffix=".unsupported")
    os.close(fd)
    try:
        save_radmesh(radmesh, temp_file, "unsupported")
    except ValueError as ve:
        # Extract the supported formats from the error message
        error_message = str(ve)
        supported_formats_str = re.search(r"Supported formats are (.+)", error_message).group(1)
        supported_formats = set(supported_formats_str.split(', '))
        
        # Compare the sets of supported formats
        assert supported_formats == {"stl", "obj", "ply", "vtk"}
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)