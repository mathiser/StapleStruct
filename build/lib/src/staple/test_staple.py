import os
import unittest
from typing import Dict

import SimpleITK as sitk
import numpy as np

from staple import bulk_staple, get_label_paths, bulk_binarize_images, save_label_images


class TestStaple(unittest.TestCase):
    def setUp(self) -> None:
        self.dicom_fol = "test_data/dcm/CT"
        self.nii_dir = "test_data/nii"
        self.staple_nii_dir = "test_data/staple/nii"
        os.makedirs(self.staple_nii_dir, exist_ok=True)

    def bulk_staple(self):
        file_dict = get_label_paths(self.nii_dir)
        d = bulk_staple(label_files_dict=file_dict, threads=4, save_otg=self.staple_nii_dir)
        self.assertIsInstance(d, Dict)
        return d

    def test_bulk_binarize_images(self):
        label_images = self.bulk_staple()
        bin_label_images = bulk_binarize_images(label_images=label_images)
        for label, image in bin_label_images.items():
            arr = sitk.GetArrayFromImage(image)
            self.assertEqual(len(np.unique(arr)), 2)
            self.assertEqual(set(np.unique(arr)), {0, 1})


if __name__ == '__main__':
    unittest.main()
