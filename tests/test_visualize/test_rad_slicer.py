import numpy as np
import pytest
from radvis.visualize.rad_slicer import RadSlicer
from tests.mocks.mock_rad_image import MockRadImage 

# Create a fixture to generate a sample RadImage object
@pytest.fixture
def rad_image():
    return MockRadImage()

# Test __init__ method and its default values
def test_init(rad_image):
    rad_slicer = RadSlicer(rad_image)
    assert rad_slicer.radimage == rad_image
    assert rad_slicer.axis == 0
    assert rad_slicer._title is None
    assert rad_slicer._cmap == "gray"
    assert rad_slicer._figsize == (4, 4)

# Test the title property
def test_title(rad_image):
    rad_slicer = RadSlicer(rad_image)
    assert rad_slicer.title == "Axis: 0"

    rad_slicer_with_title = RadSlicer(rad_image, title="Test Title")
    assert rad_slicer_with_title.title == "Test Title"