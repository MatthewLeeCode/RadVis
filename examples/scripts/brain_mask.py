import radvis as rv
import numpy as np

AXIS = 1
IMAGE_PATH = "examples/images/sub-A00028185_ses-NFB3_T1w.nii.gz"
IMAGE_MASK_PATH = "examples/images/sub-A00028185_ses-NFB3_T1w_brainmask.nii.gz"

image = rv.load_image(IMAGE_PATH)

slicer = rv.RadSlicer(image, AXIS, width=3)

mask = rv.load_image(IMAGE_MASK_PATH)
if AXIS == 2:
    mask.image_data = np.flip(mask.image_data, axis=1)
    mask.image_data = np.rot90(mask.image_data, k=1, axes=(0, 1))

slicer.add_mask(mask, color="red", alpha=0.3)

slicer.save_animation(f"images/axis_{AXIS}_brain_seg.gif", fps=30)