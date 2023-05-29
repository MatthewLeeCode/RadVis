from radvis.image.rad_image import RadImage
import numpy as np


class MockRadImage(RadImage):
    def __init__(self, file_path: str = None):
        super().__init__(file_path=file_path)
        
    def load(self, image_data: np.ndarray|None = None):
        if image_data is not None:
            image_data = np.random.rand(10, 10, 10)

        self.image_data = image_data
        return self
        
    def save(self):
        pass