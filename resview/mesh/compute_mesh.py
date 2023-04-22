""" 
This module provides abstractions over the skimage.measure.marching_cubes function
including a class to store the results.

Usage:
    Call the 'marching_cubes' function with a 3D numpy array and a threshold value.
    Additional arguments for skimage.measure.marching_cubes can be passed as keyword arguments.
    
Returns:
    A ResMesh object with the following attributes:
        vertices: A numpy array of shape (n, 3) containing the vertices of the mesh.
        faces: A numpy array of shape (m, 3) containing the faces of the mesh.
        normals: A numpy array of shape (n, 3) containing the normals of the mesh.
        values: A numpy array of shape (n,) containing the values of the mesh.
"""
import numpy as np
from skimage import measure
from typing import Any, Dict, Tuple


class ResMesh:
    """ Class to store the results of skimage.measure.marching_cubes """
    
    def __init__(self, vertices: np.ndarray, faces: np.ndarray, normals: np.ndarray, values: np.ndarray):
        self.vertices = vertices
        self.faces = faces
        self.normals = normals
        self.values = values

    def __repr__(self) -> str:
        return f"ResMesh(vertices={self.vertices.shape}, faces={self.faces.shape}, normals={self.normals.shape}, values={self.values.shape})"
        
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
        

def compute_mesh(volume: np.ndarray, threshold: float, **kwargs: Dict[str, Any]) -> ResMesh:
    """ Wrapper for skimage.measure.marching_cubes """

    if not isinstance(volume, np.ndarray) or volume.ndim != 3:
        raise ValueError("Input 'volume' must be a 3D numpy array.")
    
    if not isinstance(threshold, (int, float)):
        raise ValueError("Input 'threshold' must be a numeric value (int or float).")
    
    try:
        vertices, faces, normals, values = measure.marching_cubes(volume, threshold, **kwargs)
    except Exception as e:
        raise RuntimeError(f"Error encountered while computing marching cubes: {str(e)}")
    
    return ResMesh(vertices, faces, normals, values)
