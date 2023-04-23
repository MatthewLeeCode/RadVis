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
from typing import Any, Dict
from .rad_mesh import RadMesh        

def compute_marching_cubes(volume: np.ndarray, threshold: float, **kwargs: Dict[str, Any]) -> RadMesh:
    """ Wrapper for skimage.measure.marching_cubes """

    if not isinstance(volume, np.ndarray) or volume.ndim != 3:
        raise ValueError("Input 'volume' must be a 3D numpy array.")
    
    if not isinstance(threshold, (int, float)):
        raise ValueError("Input 'threshold' must be a numeric value (int or float).")
    
    try:
        vertices, faces, normals, values = measure.marching_cubes(volume, threshold, **kwargs)
    except Exception as e:
        raise RuntimeError(f"Error encountered while computing marching cubes: {str(e)}")
    
    return RadMesh(vertices, faces, normals, values)
