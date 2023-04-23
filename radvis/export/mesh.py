import meshio
from radvis.mesh import RadMesh

def export_radmesh(radmesh: RadMesh, file_path: str, file_format: str):
    """
    Export a RadMesh object to a specified file format.

    Args:
        radmesh (RadMesh): the RadMesh object to export
        file_path (str): the path to the output file
        file_format (str): the file format to export ('stl', 'obj', 'ply', 'collada', or 'vtk')
    """
    supported_formats = {"stl", "obj", "ply", "vtk"}

    if file_format.lower() not in supported_formats:
        raise ValueError(f"Unsupported file format '{file_format}'. Supported formats are {', '.join(supported_formats)}")

    mesh = meshio.Mesh(points=radmesh.vertices, cells=[("triangle", radmesh.faces)])
    meshio.write(file_path, mesh, file_format=file_format.lower())