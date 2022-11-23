from datetime import datetime
from zipfile import ZipFile
import base64
import os

def create_folder(folder : str):
    if not os.path.exists(folder):
        os.makedirs(folder)

def extract_extension(filename : str) -> list:
    if '.' in filename:
        return filename.split(".")
    return None

def save_base64_image(base64_image : str, folder : str,  filename : str, extension : str):
    create_folder(folder)
    image = base64.b64decode(base64_image)
    now =  datetime.now().strftime("%H-%M-%S.%f")
    filename = "{0}/{1}-{2}.{3}".format("images", filename, now, extension)
    save_file(image, filename)

def save_file(file: any, filename : str):
    with open(filename, 'wb') as writer:
        writer.write(file)

def decompress_and_save(folder : str, file : any, filename : str) -> str:
    filename, extension = extract_extension(filename)
    final_filename = "{0}/{1}".format(folder, filename)
    if 'zip' in extension.lower():
        with ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(folder)
    return final_filename