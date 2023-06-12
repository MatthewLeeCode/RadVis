from radvis.image.instantiate import load_image, from_numpy
from radvis.image.rad_image import RadImage
from radvis.image.rad_dicom_image import RadDicomImage
from radvis.image.rad_nifti_image import RadNiftiImage
from radvis.image.rad_numpy_image import RadNumpyImage
import numpy as np
import pytest


def test_load_image_unsupported_format(tmp_path):
    file_path = tmp_path / "image.jpg"
    file_path.touch()
    with pytest.raises(ValueError) as error:
        load_image(str(file_path))
    assert "Unsupported file format" in str(error.value)


def test_from_numpy():
    image_data = np.zeros((10, 10))
    image = from_numpy(image_data)
    assert isinstance(image, RadNumpyImage)
    assert np.array_equal(image.get_image_data(), image_data)