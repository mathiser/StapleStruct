import logging
from multiprocessing.pool import ThreadPool
from typing import List

import SimpleITK as sitk

from StapleStruct.utils.data_handling import LabelImages, maybe_append

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


def staple(label: str, list_of_images: List[sitk.Image]) -> (str, sitk.Image):
    fil = sitk.STAPLEImageFilter()

    fil.SetForegroundValue(255)  # Hardcoded to output of dcmrtstruct2nii
    logger.info(f"[ ] STAPLEing {label}")
    staple_img = fil.Execute(sitk.VectorOfImage(list_of_images))
    logger.info(f"[X] STAPLEing {label}")

    return label, staple_img


def bulk_staple(label_images: LabelImages, threads=1) -> LabelImages:
    t = ThreadPool(threads)
    tasks = [(label, images_list) for label, images_list in label_images.items()]
    label_images = t.starmap(staple, tasks)
    t.close()
    t.join()

    staple_dict = {}
    for label_image in label_images:
        label, image = label_image
        maybe_append(staple_dict, label, image)

    return LabelImages(staple_dict)
