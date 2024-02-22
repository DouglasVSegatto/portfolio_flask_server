import os
import shutil
import time

from flask import url_for
from pdf2image import convert_from_path


def pdf2image(upload_path, converted_path, filename):

    if not os.path.exists(converted_path):
        os.makedirs(converted_path)
    try:
        conv_images = convert_from_path(upload_path)
        for index, image in enumerate(conv_images):
            new_file = os.path.join(converted_path, f"{filename}_{index + 1}.jpg")
            print(new_file)
            image.save(new_file)
        return True
    except:
        return None


def delete_files(upload_file, download_folder):
    try:
        os.remove(upload_file)
        print(f"Folder '{upload_file}' and its contents deleted successfully.")
    except OSError as e:
        print(f"Error deleting folder '{upload_file}': {e}")

    time.sleep(180)
    try:
        shutil.rmtree(download_folder)
        print(f"Folder '{download_folder}' and its contents deleted successfully.")
    except OSError as e:
        print(f"Error deleting folder '{download_folder}': {e}")


def generate_download_link(filename_no_ext, converted_path):
    # Create a list to store download URLs
    download_urls = []
    # List the files in the directory
    print(os.listdir(converted_path))
    for filename in os.listdir(converted_path):
        file_url = url_for("download_file", folder=filename_no_ext, filename=filename)
        download_urls.append((filename, file_url))  # Store filename and download URL
    return download_urls
