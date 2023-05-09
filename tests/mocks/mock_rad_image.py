from radvis.image.rad_image import RadImage
import numpy as np


class MockRadImage(RadImage):
    def __init__(self):
        super().__init__()
        
    def load(self):
        self.image_data = np.random.rand(10, 10, 10)
        
    def save(self):
        pass