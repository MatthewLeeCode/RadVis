import numpy as np
import meshio
import os


class RadMesh:
    """ Class to store the results of skimage.measure.marching_cubes """
    
    def __init__(self, vertices: np.ndarray, faces: np.ndarray, normals: np.ndarray, values: np.ndarray):
        self.vertices = vertices
        self.faces = faces
        self.normals = normals
        self.values = values

    def __repr__(self) -> str:
        return f"RadMesh(vertices={self.vertices.shape}, faces={self.faces.shape}, normals={self.normals.shape}, values={self.values.shape})"
        
    @property
    def vertices(self) -> np.ndarray:
        """Get the vertices of the mesh."""
        return self._vertices

    @vertices.setter
    def vertices(self, vertices: np.ndarray):
        """Set the vertices of the mesh."""
        self._vertices = vertices

    @property
    def faces(self) -> np.ndarray:
        """Get the faces of the mesh."""
        return self._faces

    @faces.setter
    def faces(self, faces: np.ndarray):
        """Set the faces of the mesh."""
        self._faces = faces

    @property
    def normals(self) -> np.ndarray:
        """Get the normals of the mesh."""
        return self._normals

    @normals.setter
    def normals(self, normals: np.ndarray):
        """Set the normals of the mesh."""
        self._normals = normals

    @property
    def values(self) -> np.ndarray:
        """Get the values of the mesh."""
        return self._values

    @values.setter
    def values(self, values: np.ndarray):
        """Set the values of the mesh."""
        self._values = values
        
    def save(self, file_path: str, file_format: str):
        """
        Save the RadMesh object to a specified file format.

        Args:
            file_path (str): the path to the output file
            file_format (str): the file format to export ('stl', 'obj', 'ply', 'collada', or 'vtk')
        """
        supported_formats = {"stl", "obj", "ply", "vtk"}

        if file_format.lower() not in supported_formats:
            raise ValueError(f"Unsupported file format '{file_format}'. Supported formats are {', '.join(supported_formats)}")

        mesh = meshio.Mesh(points=self.vertices, cells=[("triangle", self.faces)], point_data={
                           "Normals": self.normals, "Values": self.values})
        meshio.write(file_path, mesh, file_format=file_format.lower())

    @classmethod
    def load(cls, file_path: str, file_format: str = None):
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
        radmesh = cls(vertices=vertices, faces=faces, normals=normals, values=values)
        return radmesh