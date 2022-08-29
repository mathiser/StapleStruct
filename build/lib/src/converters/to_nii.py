import logging
import os
import traceback
from multiprocessing.pool import ThreadPool
from typing import Dict, List

from dcmrtstruct2nii import dcmrtstruct2nii


def convert_to_nii(rtstruct_path: str, image_series_folder: str, output_folder: str):
    try:
        print(f"Converting: {rtstruct_path} to {output_folder}")
        dcmrtstruct2nii(rtstruct_file=rtstruct_path, dicom_file=image_series_folder, output_path=output_folder)

    except Exception as e:
        logging.error(e)
        traceback.print_exc()
        raise e


def bulk_convert_to_nii(rtstruct_paths: List[str], image_series_folder: str, output_folder: str, threads=1):
    try:
        tasks = []
        for i, rtstruct in enumerate(rtstruct_paths):
            tasks.append((rtstruct, image_series_folder, os.path.join(output_folder, str(i))))

        t = ThreadPool(threads)
        t.starmap(convert_to_nii, tasks)
        t.close()
        t.join()

    except Exception as e:
        logging.error(e)
        traceback.print_exc()
        raise e


