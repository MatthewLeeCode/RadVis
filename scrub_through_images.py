import radvis as rv
IMAGE_PATH = "examples/images/test_nifti.nii.gz"

image = rv.load_image(IMAGE_PATH)

slicer = rv.RadSlicer(image, 0)
slicer.display()