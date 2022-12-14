from datetime import datetime
from zipfile import ZipFile
import shutil
import base64
import os


def create_folder(folder: str):
    if not os.path.exists(folder):
        os.makedirs(folder)


def delete_folder(folder: str):
    shutil.rmtree(folder)


def extract_extension(filename: str) -> list:
    if "." in filename:
        return filename.split(".")
    return list()


def decompress_and_save(folder: str, file: any, filename: str) -> str:
    filename, extension = extract_extension(filename)
    final_filename = "{0}/{1}".format(folder, filename)
    if "zip" in extension.lower():
        with ZipFile(file, "r") as zip_ref:
            zip_ref.extractall(folder)
    return final_filename
