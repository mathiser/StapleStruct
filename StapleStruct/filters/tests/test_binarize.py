import unittest

import SimpleITK as sitk
import numpy as np

from StapleStruct.filters import bulk_binarize_images
from StapleStruct.utils.types import LabelImages


class TestStaple(unittest.TestCase):
    def setUp(self) -> None:
        self.arr = np.arange(0, 27).reshape(3, 3, 3)
        self.img = sitk.GetImageFromArray(self.arr)
        self.test_d = LabelImages({"test": [self.img]})


    def test_bulk_binarize_images(self):
        bin_label_images = bulk_binarize_images(label_images=self.test_d, binary_threshold=7)
        for label, images in bin_label_images.items():
            for image in images:
                arr = sitk.GetArrayFromImage(image)
                self.assertEqual(len(np.unique(arr)), 2)
                self.assertEqual(set(np.unique(arr)), {0, 1})


if __name__ == '__main__':
    unittest.main()
