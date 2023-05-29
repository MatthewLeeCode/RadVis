import numpy as np
from radvis.processing.filtering import percentile_clipping, noise_reduction, normalization, add_padding
from tests.mocks.mock_rad_image import MockRadImage 

def test_clipping():
    # Here, np.arange(0, 100) is reshaped to have 3D shape as the image data is 3D.
    rad_image = MockRadImage().load(image_data=np.arange(0, 100).reshape(10, 10, 1))
    clipped_image = percentile_clipping(rad_image, 0.25, 0.75)

    # Check that the clipped image data is within the specified percentiles
    lower, upper = np.percentile(rad_image.image_data, [0.25, 0.75])
    
    assert np.min(clipped_image.image_data) >= lower
    assert np.max(clipped_image.image_data) <= upper

def test_noise_reduction():
    rad_image = MockRadImage().load(image_data=np.random.normal(0, 1, size=(100, 100)))
    filtered_image = noise_reduction(rad_image, 1)
    
    # Check that the variance has decreased
    assert np.var(filtered_image.image_data) < np.var(rad_image.image_data)

def test_normalization():
    rad_image = MockRadImage().load(image_data=np.arange(0, 100))
    normalized_image = normalization(rad_image, 0, 99)
    
    # Check that the normalized image data is within the range [0, 1]
    assert np.min(normalized_image.image_data) >= 0
    assert np.max(normalized_image.image_data) <= 1

def test_add_padding():
    rad_image = MockRadImage().load(image_data=np.zeros((10, 10, 10)))
    expected_shape = (20, 20, 20)
    padded_image = add_padding(rad_image, expected_shape)

    # Check that the shape matches the expected shape
    assert padded_image.image_data.shape == expected_shape

