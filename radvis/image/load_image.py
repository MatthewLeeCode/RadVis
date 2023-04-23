from .rad_image import RadImage
from .rad_dicom_image import RadDicomImage
from .rad_nifti_image import RadNiftiImage
import os

def load_image(file_path: str) -> RadImage:
    """
    Infer the file format of the image and load it using the appropriate RadImage subclass.

    :param file_path: The file path to the image file
    :return: An instance of a RadImage subclass for the corresponding file format
    """
    abs_path = os.path.abspath(file_path)
    _, extension = os.path.splitext(abs_path)
    extension = extension.lower()

    if extension == ".dcm":
        return RadDicomImage(abs_path)
    elif extension in (".nii", ".nii.gz"):
        return RadNiftiImage(abs_path)
    else:
        raise ValueError(f"Unsupported file format: {extension}")
