# RadVis
RadVis (Radiology Visualization) is a visualization tool for medical images.

> Work in progress

Currently implemented features:
- Load both DICOM and NIFTI images
- Can display 2D slices of the 3D images
- Ability to add a mask to the image
- Works in both notebooks and scripts

## Installation
`pip install radvis`

## Usage

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
# slicer.save_animation(f"images/axis_{AXIS}_brain_seg.gif", fps=30)
```

<p float="left">
  <img src="https://raw.githubusercontent.com/medlee-code/RadVis/main/images/axis_1_brain_seg.gif?token=GHSAT0AAAAAACBJZC7PZ2WT3CJ26PONDN2YZC7T46Q" width="49%" /> 
  <img src="https://raw.githubusercontent.com/medlee-code/RadVis/main/images/axis_2_brain_seg.gif?token=GHSAT0AAAAAACBJZC7PDVRWL2CW2OCTUV3CZC7T5BQ" width="49%" />
</p>