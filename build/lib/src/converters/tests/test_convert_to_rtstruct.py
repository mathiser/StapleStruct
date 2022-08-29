import unittest

from converters import convert_to_rtstruct
from staple.staple import get_label_paths, get_label_images_from_label_paths


class TestToRTSTRUCT(unittest.TestCase):
    def setUp(self) -> None:
        self.dicom_fol = "test_data/dcm/CT"
        self.nii_dir = "test_data/staple/binary"
        self.label_paths = get_label_paths(self.nii_dir)
        self.label_images = get_label_images_from_label_paths(self.label_paths)

    def test_convert_to_rtstruct(self):
        label_images = get_label_images_from_label_paths(self.label_paths)
        convert_to_rtstruct(label_images=label_images, image_series_folder=self.dicom_fol, output_folder=".")

if __name__ == '__main__':
    unittest.main()
