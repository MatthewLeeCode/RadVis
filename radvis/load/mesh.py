import meshio
from radvis.mesh import RadMesh
import os

def load_radmesh(file_path: str, file_format: str = None) -> RadMesh:
    """
    Import a mesh file in a specified format and convert it to a RadMesh object.

    Args:
    file_path (str): the path to the input file
    file_format (str, optional): the file format to import ('stl', 'obj', 'ply', 'collada', or 'vtk'). 
        If not provided, it will be inferred from the file extension.

    Returns:
    RadMesh: the imported RadMesh object
    """
    supported_formats = ["stl", "obj", "ply", "vtk"]

    if file_format:
        file_format = file_format.lower()
        if file_format not in supported_formats:
            raise ValueError(f"Unsupported file format '{file_format}'. Supported formats are {', '.join(supported_formats)}")
    else:
        ext = os.path.splitext(file_path)[1][1:].lower()
        if ext not in supported_formats:
            raise ValueError(f"Unsupported file format '{ext}'. Supported formats are: {', '.join(supported_formats)}")
        file_format = ext

    mesh = meshio.read(file_path, file_format=file_format)

    # Extract vertices, faces, normals, and values from the mesh
    vertices = mesh.points
    faces = mesh.get_cells_type("triangle")
    normals = mesh.point_data.get("Normals", None)
    values = mesh.point_data.get("Values", None)

    # Create and return a RadMesh object
    radmesh = RadMesh(vertices=vertices, faces=faces, normals=normals, values=values)
    return radmesh