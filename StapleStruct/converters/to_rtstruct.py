import os
from typing import List, Dict

import SimpleITK as sitk
import pydicom
from rt_utils import RTStructBuilder
from staple.staple import LabelImages

def convert_to_rtstruct(label_images: LabelImages, image_series_folder: str, output_folder: str) -> str:
    rtstruct = RTStructBuilder.create_new(dicom_series_path=image_series_folder)
    for label, img in label_images.items():
        mask_arr = sitk.GetArrayFromImage(img)
        mask_arr = mask_arr.transpose([1, 2, 0]).astype(bool)
        rtstruct.add_roi(
            mask=mask_arr,
            name=label
        )
    ds = pydicom.dcmread(os.path.join(image_series_folder, os.listdir(image_series_folder)[0]))
    out_file = os.path.join(output_folder, f"{ds.PatientID}")
    rtstruct.save(out_file)
    return out_file