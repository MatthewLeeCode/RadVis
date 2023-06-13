import numpy as np
from radvis.processing.image import percentile_clipping, noise_reduction, normalization, add_padding, apply_mask
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

def test_apply_mask():
    # Create a mock image with a diagonal line of 1s
    image_data = np.zeros((10, 10))
    np.fill_diagonal(image_data, 1)
    rad_image = MockRadImage().load(image_data=image_data)

    # Create a mask that selects the diagonal line
    mask = np.eye(10)

    # Apply the mask to the image
    masked_image = apply_mask(rad_image, mask)

    # Check that the masked image only has values on the diagonal line
    assert np.array_equal(masked_image.image_data, np.eye(10))

def test_apply_mask_invert():
    # Create a mock image with a diagonal line of 1s
    image_data = np.zeros((10, 10))
    np.fill_diagonal(image_data, 1)
    rad_image = MockRadImage().load(image_data=image_data)

    # Create a mask that selects everything except the diagonal line
    mask = np.ones((10, 10)) - np.eye(10)

    # Apply the inverted mask to the image
    masked_image = apply_mask(rad_image, mask, invert=True)

    # Check that the masked image only has values off the diagonal line
    assert np.array_equal(masked_image.image_data, np.ones((10, 10)) - np.eye(10))
