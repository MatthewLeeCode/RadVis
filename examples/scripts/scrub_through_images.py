import sys
sys.path.append("../../")

import radvis as rv
import numpy as np

IMAGE_PATH = "../images/test_nifti.nii.gz"

image = rv.load_image(IMAGE_PATH)

slicer = rv.RadSlicer(image, 2)

red_mask = np.zeros_like(image.image_data) 
red_mask[5:100, 5:100, 5:100] = 1

blue_mask = np.zeros_like(image.image_data)
blue_mask[70:150, 70:150, 70:150] = 1

slicer.add_mask(red_mask, color="red")
slicer.add_mask(blue_mask, color="blue")

slicer.display()