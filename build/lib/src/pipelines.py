import argparse
import os

from converters import bulk_convert_to_nii
from staple.staple import get_label_paths, get_label_images_from_label_paths, bulk_binarize_images, bulk_staple

def rtstruct_to_nii():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--input_folder', required=True, help="")
    parser.add_argument('-o', "--output_folder", required=True, help="")

    args = parser.parse_args()
    input = args.input_json
    output = args.output_zip_path


def nii_to_rtstruct():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--input_folder', required=True, help="")
    parser.add_argument('-o', "--output_folder", required=True, help="")

    args = parser.parse_args()
    input = args.input_json
    output = args.output_zip_path

def staple_nii():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--input_folder', required=True, help="")
    parser.add_argument('-o', "--output_folder", required=True, help="")

    args = parser.parse_args()
    input = args.input_json
    output = args.output_zip_path
def binarize_staple_heatmaps():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--input_folder', required=True, help="")
    parser.add_argument('-o', "--output_folder", required=True, help="")

    args = parser.parse_args()
    input = args.input_json
    output = args.output_zip_path

def staple_rtstructs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--input_folder', required=True, help="")
    parser.add_argument('-o', "--output_folder", required=True, help="")

    args = parser.parse_args()
    input = args.input_json
    output = args.output_zip_path
