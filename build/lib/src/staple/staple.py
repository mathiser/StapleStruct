import logging
import os
import traceback
from multiprocessing.pool import ThreadPool
from typing import Dict, List, NewType

import SimpleITK as sitk

LabelPaths = NewType("LabelPaths", Dict[str, List[str]])
LabelImages = NewType("LabelImages", Dict[str, sitk.Image])

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


def staple(label: str, list_of_images: List[sitk.Image], save_otg=None) -> (str, sitk.Image):
    fil = sitk.STAPLEImageFilter()

    fil.SetForegroundValue(255)  # Hardcoded to output of dcmrtstruct2nii
    logger.info(f"[ ] STAPLEing {label}")
    staple_img = fil.Execute(sitk.VectorOfImage(list_of_images))
    staple_img.CopyInformation(list_of_images[0])
    logger.info(f"[X] STAPLEing {label}")
    if save_otg:
        save_image(label, staple_img, save_otg)
        save_image("binary"+label, binarize_image(staple_img), save_otg)

    return label, staple_img


def binarize_image(image: sitk.Image, threshold=0.5) -> sitk.Image:
    return image > threshold


def bulk_binarize_images(label_images: LabelImages, save_otg: str = None) -> LabelImages:
    new = {}
    for label, image in label_images.items():
        logger.info(f"[ ] Binarizing {label}, {image.GetSize()}")
        bin_img = binarize_image(image)
        new[label] = bin_img
        logger.info(f"[X] Binarizing {label}")
        if save_otg:
            save_image(label, bin_img, save_otg)

    return LabelImages(new)


def bulk_staple(label_files_dict: LabelPaths, threads=1, save_otg: str = None) -> LabelImages:
    tasks = []
    for label, paths in label_files_dict.items():
        tasks.append((label, [sitk.ReadImage(path) for path in paths], save_otg))

    t = ThreadPool(threads)
    label_images = t.starmap(staple, tasks)
    t.close()
    t.join()

    staple_dict = {}
    for label_image in label_images:
        label, image = label_image
        staple_dict[label] = image

    return LabelImages(staple_dict)


def get_label_paths(nifti_path: str) -> LabelPaths:
    match_dict = {}
    for fol, subs, files in os.walk(nifti_path):
        for file in files:
            if file.endswith(".nii.gz") and "image" not in file:
                oar = file.replace(".nii.gz", "").replace("mask_", "")
                if oar not in match_dict.keys():
                    match_dict[oar] = [os.path.join(fol, file)]
                else:
                    match_dict[oar].append(os.path.join(fol, file))

    return LabelPaths(match_dict)


def get_label_images_from_label_paths(label_paths: LabelPaths) -> LabelImages:
    label_images = {}
    for label, path in label_paths.items():
        img = sitk.ReadImage(path)
        if img.GetDimension() == 4:  # Fight a SimpleITK bug! An empty 4th dimension is loaded for some unknown reason.
            img = img[:, :, :, 0]


        label_images[label] = img
    return LabelImages(label_images)


def save_image(label: str, image: sitk.Image, output_folder: str):
    logger.info(f"[ ] Saving {label}")
    sitk.WriteImage(image, os.path.join(output_folder, f"{label}.nii.gz"))
    logger.info(f"[X] Saving {label}")


def save_label_images(label_images: LabelImages, output_folder):
    try:
        for label, image in label_images.items():
            save_image(label, image, output_folder)
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        raise e
