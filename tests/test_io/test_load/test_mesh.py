import os
import tempfile
import numpy as np
from radvis.mesh import RadMesh
from radvis.io.save.mesh import save_radmesh
from radvis.io.load.mesh import load_radmesh

def create_test_radmesh():
    vertices = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

    faces = np.array([
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 1],
        [1, 2, 3]
    ])
    
    normals = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 1, 1]])
    values = np.array([0.0, 0.5, 1.0, 1.5])

    return RadMesh(vertices=vertices, faces=faces, normals=normals, values=values)

def test_load_radmesh_supported_format():
    radmesh = create_test_radmesh()
    supported_formats = ["stl", "obj", "ply", "vtk"]

    for file_format in supported_formats:
        fd, temp_file_path = tempfile.mkstemp(suffix=f".{file_format}")
        os.close(fd)
        try:
            # Export the radmesh to a temporary file
            save_radmesh(radmesh, temp_file_path, file_format)

            # Import the radmesh from the temporary file and check its properties
            imported_radmesh = load_radmesh(temp_file_path, file_format)
            assert np.allclose(radmesh.vertices, imported_radmesh.vertices)
            assert np.array_equal(radmesh.faces, imported_radmesh.faces)
        finally:
            os.remove(temp_file_path)

def test_load_radmesh_unsupported_format():
    with tempfile.NamedTemporaryFile(suffix=".unsupported") as temp_file:
        try:
            load_radmesh(temp_file.name, "unsupported")
        except ValueError as ve:
            assert str(ve) == "Unsupported file format 'unsupported'. Supported formats are stl, obj, ply, vtk"

