import ipyvolume as ipv
from radvis.mesh import RadMesh
import numpy as np


def create_figure() -> ipv.Figure:
    """
    Create an empty ipyvolume figure.

    :return: An empty ipyvolume figure.
    """
    fig = ipv.figure()
    return fig


def add_mesh(fig: ipv.Figure, radmesh: RadMesh, color: str = 'orange') -> ipv.Figure:
    """
    Add a mesh from a RadMesh object to an ipyvolume figure.

    :param fig: The ipyvolume figure to add the mesh to.
    :param radmesh: The RadMesh object containing the mesh data.
    :param color: The color of the mesh, can be a hex or RGB value. Default is 'orange'.
    :return: The ipyvolume figure with the mesh added.
    """
    mesh_color = ipv.plot_trisurf(radmesh.vertices[:, 0], radmesh.vertices[:, 1], radmesh.vertices[:, 2], triangles=radmesh.faces, color=color)
    mesh_color.material.color = color
    return fig


def add_volume(fig: ipv.Figure, volume_data: np.ndarray) -> ipv.Figure:
    """
    Add volume data to an ipyvolume figure.

    :param fig: The ipyvolume figure to add the volume data to.
    :param volume_data: 3D numpy array representing the voxel data.
    :return: The ipyvolume figure with the volume data added.
    """
    ipv.volshow(volume_data, level=[0.1, 0.5, 0.9], opacity=[0.01, 0.05, 0.1], level_width=0.1, data_min=0, data_max=1)
    return fig


def show_figure(fig: ipv.Figure, azimuth: float = 30, elevation: float = 30, distance: float = 2) -> ipv.Figure:
    """
    Set camera angle and display the ipyvolume figure.

    :param fig: The ipyvolume figure to display.
    :param azimuth: The azimuth angle of the camera. Default is 30.
    :param elevation: The elevation angle of the camera. Default is 30.
    :param distance: The distance of the camera from the center. Default is 2.
    :return: The displayed ipyvolume figure.
    """
    ipv.view(azimuth=azimuth, elevation=elevation, distance=distance)
    ipv.show()
    return fig
