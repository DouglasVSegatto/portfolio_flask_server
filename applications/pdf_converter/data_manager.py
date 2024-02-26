import os
import shutil
import time
from builtins import FileNotFoundError

import img2pdf
from flask import url_for
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFSyntaxError

from global_functions import (download_file_path, remove_extension,
                              upload_file_path)


def pdf2image(filename):
    """
    Converts PDF file to Image

    First: Checks for an existing destination folder, if doesn't exist, it creates a folder.
    Second: File is converted to JPG and saved at folder from First step by utilizing the pdf2image converter

    :param filename: contains original file name uploaded, used to delete file and folder
    :type filename: str
    :return: True if the conversion is successful, False otherwise.
    :rtype: boolean
    """
    download_path = download_file_path(remove_extension(filename))
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    try:
        conv_images = convert_from_path(upload_file_path(filename))
        for index, image in enumerate(conv_images):
            new_file = os.path.join(download_file_path(remove_extension(filename)),
                                    f'{remove_extension(filename)}_{index + 1}.jpg')
            image.save(new_file)
        return True
    except (IOError, FileNotFoundError, PDFSyntaxError):
        return False


def image2pdf(filename):
    """
    Converts Image files to PDF

    First: Checks for an existing destination folder, if doesn't exist, it creates a folder.
    Second: File is converted to PDF and saved at folder from First step by utilizing the img2pdf converter

    :param filename: contains original file name uploaded, used to delete file and folder
    :type filename: str
    :return: True if the conversion is successful, False otherwise.
    :rtype: boolean
    """

    download_path = download_file_path(remove_extension(filename))
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    try:
        file_path = os.path.join(download_path, f"{remove_extension(filename)}.pdf")
        with open(file_path, "wb") as f:
            f.write(img2pdf.convert(open(upload_file_path(filename), "rb")))
        return True
    except (IOError, FileNotFoundError, PDFSyntaxError):
        return False


def delete_files(filename):
    """
    Deletes the specified file to ensure no unnecessary data is retained and to save storage space
    Uploaded file and folder containing files converted are deleted.

    :param filename: contains original file name uploaded, used to delete file and folder
    :type filename: str
    :return: None
    :rtype: None

    PS: Keeping in print as current server doesn't have log available
    """

    try:
        os.remove(upload_file_path(filename))
        print(f"File '{remove_extension(filename)}' deleted successfully.")
    except OSError as e:
        print(f"Error deleting file '{remove_extension(filename)}': {e}")

    time.sleep(180)
    try:
        shutil.rmtree(download_file_path(remove_extension(filename)))
        print(f"Folder '{download_file_path(remove_extension(filename))}' and its contents were deleted successfully.")
    except OSError as e:
        print(f"Error deleting folder '{download_file_path(remove_extension(filename))}': {e}")


def generate_download_link(filename):
    """
    Generates a list,
    Each file found will generate an extra list containing the filename and its corresponding download URL.

    :param filename: Contains original file name uploaded, used to delete file and folder
    :type filename: str
    :return: A list, each containing the filename and its download URL.
    :rtype:list[(str, str)]
    """
    download_urls = []
    for file_found in os.listdir(download_file_path(remove_extension(filename))):
        file_url = url_for("download_file", folder=remove_extension(filename), filename=file_found)
        download_urls.append((file_found, file_url))  # Store filename and download URL
    return download_urls
