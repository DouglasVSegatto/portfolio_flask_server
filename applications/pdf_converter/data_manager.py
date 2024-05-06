import os
from builtins import FileNotFoundError

import img2pdf
from flask import url_for
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFSyntaxError, PDFPageCountError

from global_functions import download_file_path, remove_extension, upload_file_path

from pypdf import PdfWriter


def convert_pdf2image(folder_name):
    """
    Converts PDF file to Image

    First: Checks for an existing destination folder, if doesn't exist, it creates a folder.
    Second: File is converted to JPG and saved at folder from First step by utilizing the pdf2image converter

    :param folder_name: contains original file name uploaded, used to delete file and folder
    :type folder_name: str
    :return: True if the conversion is successful, else: False.
    :rtype: boolean

    :raises IOError: If an I/O error occurs during file operations.
    :raises FileNotFoundError: If the specified folder or any of its contents cannot be found.
    :raises PDFSyntaxError: If there is a syntax error in the input PDF file.
    """
    try:
        files = os.listdir(upload_file_path(folder_name))
        for file_name in files:
            convert_from_path(
                pdf_path=upload_file_path(folder_name, file_name),
                output_folder=download_file_path(folder_name),
                output_file=remove_extension(file_name),
                fmt="jpg",
            )
        return True
    except (IOError, FileNotFoundError, PDFSyntaxError, PDFPageCountError) as e:
        print(f"Error occurred: {e}")
        return False


def convert_image2pdf(folder_name):
    """
    Converts Image files to PDF

    First: Checks for an existing destination folder, if doesn't exist, it creates a folder.
    Second: File is converted to PDF and saved at folder from First step by utilizing the img2pdf converter

    :param folder_name: contains original file name uploaded, used to delete file and folder
    :type folder_name: str

    :return: True if the conversion is successful, False otherwise.
    :rtype: boolean

    :raises IOError: If an I/O error occurs during file operations.
    :raises FileNotFoundError: If the specified folder or any of its contents cannot be found.
    """
    try:
        capture_name = os.listdir(upload_file_path(folder_name))
        imgs = []
        for file_name in os.listdir(upload_file_path(folder_name)):
            imgs.append(upload_file_path(folder_name=folder_name, file_name=file_name))
        first_file_name = remove_extension(capture_name[0])
        with open(f"{download_file_path(folder_name, first_file_name)}.pdf", "wb") as f:
            f.write(img2pdf.convert(imgs))
        return True
    except (IOError, FileNotFoundError) as e:
        print(f"Error occurred: {e}")
        return False


def pdf_merge(folder_name):
    """
    Merges PDF files located in a specified folder into a single PDF file.

    First: Checks for the existence of the folder containing PDF files.
    Second: PDF files are appended to a PdfWriter object for merging.
    Third: The merged PDF file is saved at the folder location from the First step.

    :param folder_name: The name of the folder containing the PDF files to be merged.
    :type folder_name: str

    :return: True if the merging process is successful, False otherwise.
    :rtype: bool

    :raises IOError: If an I/O error occurs during file operations.
    :raises FileNotFoundError: If the specified folder or any of its contents cannot be found.
    """
    merge = PdfWriter()
    try:
        files = os.listdir(upload_file_path(folder_name))
        first_file_name = files[0]
        for pdf in files:
            merge.append(upload_file_path(folder_name, pdf))

        with open(download_file_path(folder_name, first_file_name), "wb") as f:
            merge.write(f)
        return True
    except (IOError, FileNotFoundError) as e:
        print(f"Error occurred: {e}")


def generate_download_link(folder_name):
    """
    Generates a list,
    Each file found will generate an extra list containing the filename and its corresponding download URL.

    :param folder_name: Contains original file name uploaded, used to delete file and folder
    :type folder_name: str
    :return: A list, each containing the filename and its download URL.
    :rtype:list[(str, str)]
    """
    download_urls = []
    for file_found in os.listdir(download_file_path(folder_name)):
        file_url = url_for("download_file", folder=folder_name, filename=file_found)
        download_urls.append((file_found, file_url))  # Store filename and download URL
    return download_urls
