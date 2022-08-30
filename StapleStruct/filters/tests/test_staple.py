import unittest
from typing import Dict

from StapleStruct.filters import bulk_staple
from StapleStruct.utils import get_label_paths, get_label_images_from_label_paths


class TestStaple(unittest.TestCase):
    def setUp(self) -> None:
        self.nii_dir = "/home/mathis/projects/repos/StapleStruct_test_data/nii"

    def test_bulk_staple(self):
        file_dict = get_label_paths(self.nii_dir)
        label_images = get_label_images_from_label_paths(file_dict)
        d = bulk_staple(label_images=label_images, threads=8)
        self.assertIsInstance(d, Dict)
        return d

if __name__ == '__main__':
    unittest.main()
