import os
from typing import List

from StapleStruct.converters import bulk_convert_to_nii
from StapleStruct.filters import bulk_staple, bulk_binarize_images
from StapleStruct.utils.data_handling import save_label_images, get_label_paths, get_label_images_from_label_paths


def staple_struct(rtstruct_paths: List[str],
                  image_series_folder: str,
                  output_folder: str,
                  binary_threshold: float = 0.90,
                  threads=8):

    # Convert RTSTRUCTs to nifti
    nii = os.path.join(output_folder, "nifti")
    staple_raw = os.path.join(output_folder, "staple_raw")
    staple_bin = os.path.join(output_folder, "staple_bin")
    for folder in [nii, staple_bin, staple_raw]:
        os.makedirs(folder, exist_ok=True)

    bulk_convert_to_nii(rtstruct_paths=rtstruct_paths,
                        image_series_folder=image_series_folder,
                        output_folder=nii,
                        threads=threads)

    # STAPLE outputs
    paths = get_label_paths(nii)
    label_images = get_label_images_from_label_paths(paths)
    label_images = bulk_staple(label_images=label_images, threads=threads)
    # Save STAPLEs
    save_label_images(label_images=label_images, output_folder=staple_raw)

    # Binarize and save STAPLEs
    bin_images = bulk_binarize_images(label_images=label_images, binary_threshold=binary_threshold)
    save_label_images(label_images=bin_images, output_folder=staple_bin)
