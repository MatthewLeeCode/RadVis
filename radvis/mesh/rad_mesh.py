import numpy as np

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