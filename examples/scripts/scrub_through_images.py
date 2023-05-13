import radvis as rv
import numpy as np

image = rv.load_image('examples/images/sub-A00028185_ses-NFB3_T1w.nii.gz')

slicer = rv.RadSlicer(image, axis=0)

# 0 values wont be displayed
red_mask = np.zeros_like(image.image_data) 
red_mask[5:100, 5:100, 5:100] = 1

blue_mask = np.zeros_like(image.image_data)
blue_mask[70:150, 70:150, 70:150] = 1

slicer.add_mask(red_mask, color="red")
slicer.add_mask(blue_mask, color="blue")

slicer.save_animation("images/example_mask_0.gif", fps=30)