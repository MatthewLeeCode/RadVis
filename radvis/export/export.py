import meshio
from radvis.mesh import RadMesh

def export_stl(radmesh: RadMesh, file_path: str):
    """
    Export a RadMesh object to an STL file.

    Args:
        radmesh (RadMesh): the RadMesh object to export
        file_path (str): the path to the output STL file
    """
    mesh = meshio.Mesh(points=radmesh.vertices, cells=[("triangle", radmesh.faces)])
    meshio.write(file_path, mesh, file_format="stl")

def export_obj(radmesh: RadMesh, file_path: str):
    """
    Export a RadMesh object to a Wavefront OBJ file.

    Args:
        radmesh (RadMesh): the RadMesh object to export
        file_path (str): the path to the output OBJ file
    """
    mesh = meshio.Mesh(points=radmesh.vertices, cells=[("triangle", radmesh.faces)])
    meshio.write(file_path, mesh, file_format="obj")

def export_ply(radmesh: RadMesh, file_path: str):
    """
    Export a RadMesh object to a PLY file.

    Args:
        radmesh (RadMesh): the RadMesh object to export
        file_path (str): the path to the output PLY file
    """
    mesh = meshio.Mesh(points=radmesh.vertices, cells=[("triangle", radmesh.faces)])
    meshio.write(file_path, mesh, file_format="ply")

def export_collada(radmesh: RadMesh, file_path: str):
    """
    Export a RadMesh object to a COLLADA file.

    Args:
        radmesh (RadMesh): the RadMesh object to export
        file_path (str): the path to the output COLLADA file
    """
    mesh = meshio.Mesh(points=radmesh.vertices, cells=[("triangle", radmesh.faces)])
    meshio.write(file_path, mesh, file_format="collada")

def export_vtk(radmesh: RadMesh, file_path: str):
    """
    Export a RadMesh object to a VTK file.

    Args:
        radmesh (RadMesh): the RadMesh object to export
        file_path (str): the path to the output VTK file
    """
    mesh = meshio.Mesh(points=radmesh.vertices, cells=[("triangle", radmesh.faces)])
    meshio.write(file_path, mesh, file_format="vtk")