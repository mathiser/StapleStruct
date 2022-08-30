import logging
from multiprocessing.pool import ThreadPool
from typing import Tuple

import SimpleITK as sitk

from StapleStruct.utils.data_handling import LabelImages, maybe_append

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


def bulk_binarize_images(label_images: LabelImages, binary_threshold: float, threads: int = 1) -> LabelImages:
    t = ThreadPool(threads)
    tasks = [(label, image, binary_threshold) for label, images in label_images.items() for image in images]
    label_images = t.starmap(binarize_image, tasks)
    t.close()
    t.join()

    bin_dict = {}
    for label_image in label_images:
        label, image = label_image
        maybe_append(bin_dict, label, image)

    return LabelImages(bin_dict)


def binarize_image(label, image: sitk.Image, threshold=0.5) -> Tuple[str, sitk.Image]:
    logger.info(f"[ ] Binarizing {label}, {image.GetSize()}")
    bin_img = image > threshold
    logger.info(f"[X] Binarizing {label}")

    return label, bin_img
