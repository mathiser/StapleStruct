import os
import tempfile
import unittest

from converters import convert_to_nii, bulk_convert_to_nii


class TestConverters(unittest.TestCase):
    def setUp(self) -> None:
        self.rtstruct_paths = [os.path.join(fol, file) for fol, subs, files in os.walk("test_data/dcm/RTSTRUCT") for
                               file in files]
        self.rtstruct_path = self.rtstruct_paths[0]
        self.dicom_fol = "test_data/dcm/CT"
        self.nii_dir = "test_data/nii"


    def test_convert_to_nii(self):
        with tempfile.TemporaryDirectory(dir=".") as tmp_folder:
            b = convert_to_nii(rtstruct_path=self.rtstruct_path,
                               image_series_folder=self.dicom_fol,
                               output_folder=tmp_folder)
            self.assertTrue(b)

    def test_convert_to_nii_error(self):
        with tempfile.TemporaryDirectory(dir=".") as tmp_folder:
            b = convert_to_nii(rtstruct_path="self.rtstruct_path",
                               image_series_folder="self.dicom_fol",
                               output_folder="tmp_folder")
            self.assertFalse(b)

    def test_bulk_to_nii(self):
        with tempfile.TemporaryDirectory(dir=".") as tmp_folder:
            b = bulk_convert_to_nii(rtstruct_paths=self.rtstruct_paths,
                                    image_series_folder=self.dicom_fol,
                                    output_folder=tmp_folder)
            self.assertTrue(b)





if __name__ == '__main__':
    unittest.main()
