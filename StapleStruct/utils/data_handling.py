import logging
import os
import traceback

import SimpleITK as sitk

from StapleStruct.utils.types import LabelPaths, LabelImages

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


def get_label_paths(nifti_path: str) -> LabelPaths:
    match_dict = {}
    for fol, subs, files in os.walk(nifti_path):
        for file in files:
            if file.endswith(".nii.gz") and "image" not in file:
                oar = file.replace(".nii.gz", "").replace("mask_", "")
                maybe_append(match_dict, oar, os.path.join(fol, file))

    return LabelPaths(match_dict)


def get_label_images_from_label_paths(label_paths: LabelPaths) -> LabelImages:
    label_images = {}
    for label, paths in label_paths.items():
        for path in paths:
            img = sitk.ReadImage(path)
            # if img.GetDimension() == 4:  # Fight a SimpleITK bug! An empty 4th dimension is loaded for some unknown reason.
            #    img = img[:, :, :, 0]

            maybe_append(label_images, label, img)

    return LabelImages(label_images)


def maybe_append(dict, key, value):
    if key in dict.keys():
        dict[key].append(value)
    else:
        dict[key] = [value]


def save_image(label: str, image: sitk.Image, output_folder: str):
    logger.info(f"[ ] Saving {label}")
    sitk.WriteImage(image, os.path.join(output_folder, f"{label}.nii.gz"))
    logger.info(f"[X] Saving {label}")


def save_label_images(label_images: LabelImages, output_folder):
    try:
        for label, images in label_images.items():
            for i, image in enumerate(images):
                oi = os.path.join(output_folder, str(i))
                os.makedirs(oi, exist_ok=True)
                save_image(label, image, oi)
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        raise e
