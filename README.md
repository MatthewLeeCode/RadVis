# RadVis
RadVis (Radiology Visualization) is a visualization tool for medical images.

Currently implemented features:
- Load both DICOM and NIFTI images
- Can display 2D slices of the 3D images
- Ability to add a mask to the image
- Works in both notebooks and scripts

## Installation
`pip install radvis`

## RadSlice Viewer

Loading an image and displaying it with a slider
```python
import radvis as rv

# Creates a 'RadImage' object containing the image data
image = rv.load_image('path/to/image.nii.gz')

slicer = rv.RadSlicer(image, axis=0)

slicer.display()
```
![](https://raw.githubusercontent.com/medlee-code/RadVis/main/images/example_0.gif?token=GHSAT0AAAAAACBJZC7OUK4KUWZ4QWBJIGJ6ZC7T4HA)

Adding masks to the image
```python
import radvis as rv
import numpy as np

image = rv.load_image('path/to/image.nii.gz')

slicer = rv.RadSlicer(image, axis=0)

# 0 values wont be displayed
red_mask = np.zeros_like(image.image_data) 
red_mask[5:100, 5:100, 5:100] = 1

blue_mask = np.zeros_like(image.image_data)
blue_mask[70:150, 70:150, 70:150] = 1

slicer.add_mask(red_mask, color="red")
slicer.add_mask(blue_mask, color="blue")

slicer.display()
```
![](https://raw.githubusercontent.com/medlee-code/RadVis/main/images/example_mask_0.gif?token=GHSAT0AAAAAACBJZC7OHBDQFXT7KM5L42NUZC7T4SQ)

Mask can be another RadImage object so you can load up your masks from a DICOM or NIFTI
```python
import radvis as rv
import numpy as np

AXIS = 1
IMAGE_PATH = "path/to/image.nii.gz"
IMAGE_MASK_PATH = "path/to/mask.nii.gz"

image = rv.load_image(IMAGE_PATH)
mask = rv.load_image(IMAGE_MASK_PATH)

slicer = rv.RadSlicer(image, AXIS, width=3)
slicer.add_mask(mask, color="red", alpha=0.3)

slicer.display()
slicer.save_animation(f"images/axis_{AXIS}_brain_seg.gif", fps=30)
slicer.save_frame(f"images/axis_{AXIS}_brain_seg.png", index=180, dpi=300)
```

<p float="left">
  <img src="https://raw.githubusercontent.com/medlee-code/RadVis/main/images/axis_1_brain_seg.gif?token=GHSAT0AAAAAACBJZC7PZ2WT3CJ26PONDN2YZC7T46Q" width="49%" /> 
  <img src="https://raw.githubusercontent.com/medlee-code/RadVis/main/images/axis_2_brain_seg.gif?token=GHSAT0AAAAAACBJZC7PDVRWL2CW2OCTUV3CZC7T5BQ" width="49%" />
</p>

## Processing Module

The processing module of RadVis offers a set of functions to perform preprocessing tasks

### Clipping
The `percentile_clipping` function allows you to clip the pixel intensities of an image at specified lower and upper percentiles. This can be helpful in enhancing the contrast of the image.

### Noise Reduction
The `noise_reduction` function can be used to reduce the amount of noise in your images, which is particularly useful for medical images where noise can often interfere with the analysis.

### Normalization
The `normalization` function is used to normalize the pixel intensities of the image to a specified range. This is useful for preparing your images for machine learning models, which often perform better when the input data is normalized.

### Padding
The `add_padding` function can be used to add padding to your images, which can be useful when you need to make all your images the same size for subsequent analysis or to apply a neural network that requires input images to be of a certain size.

Example usage of processing functions:

```python
import radvis as rv
import numpy as np

# Loading image
image = rv.load_image(filepath='path/to/image.nii.gz')

# Applying processing functions
clipped_image = rv.processing.percentile_clipping(image, lower_percentile=0.25, upper_percentile=0.75)
filtered_image = rv.processing.noise_reduction(clipped_image, filter_size=1)
normalized_image = rv.processing.normalization(filtered_image, min_val=0, max_val=255)
padded_image = rv.processing.add_padding(normalized_image, target_shape=(128, 128, 128))

# Displaying processed image
slicer = rv.RadSlicer(padded_image, axis=0)
slicer.display()
```