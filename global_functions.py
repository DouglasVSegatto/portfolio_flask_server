import locale
import os
import uuid
import shutil
import time

"""
Created this 'global_functions' as few can be reused many times by other apps.
"""


def remove_extension(file_name):
    """
    Remove the file extension from the given filename and return the main name.

    :param file_name: Contains original filename uploaded, including its extension.
    :type file_name: str
    :return: The main filename without the extension.
    :rtype: str
    """
    return os.path.splitext(file_name)[0]


def upload_file_path(folder_name, file_name=None):
    """
    Creates os path for upload folder with filename, including its extension

    :param folder_name: Contains the name/folder_id generated.
    :type folder_name: str
    :param file_name: Contains original filename uploaded, including its extension.
    :type file_name: str

    if file_name:
        :return: Path to uploaded file
    else:
        :return: Path to folder_name
    :rtype: str
    """
    if file_name:
        return os.path.join("static", "upload", folder_name, file_name)
    else:
        return os.path.join("static", "upload", folder_name)


def download_file_path(folder_name, file_name=None):
    """
    Creates os path for download folder with filename:
        Tracking folder - filename must be passed without its extension.
        Tracking file - filename must be passed including its extension.

    :param folder_name: Contains the name/folder_id generated.
    :type folder_name: str
    :param file_name: Contains original filename uploaded, including its extension.
    :type file_name: str

    if file_name:
        :return: Path to uploaded file
    else:
        :return: Path to folder_name
    :rtype: str
    """

    if file_name:
        return os.path.join("static", "download", folder_name, file_name)
    else:
        return os.path.join("static", "download", folder_name)


def set_punctuation(value):
    """
    Format args value with punctuation.

    :param value: The numeric value to be formatted with punctuation.
    :type value: float
    :return: The formatted value with punctuation proper punctuation.
    :rtype: str

    Example:
    set_punctuation(1234567.89)
    '1,234,567.9'
    """
    locale.setlocale(locale.LC_ALL, "")
    value_formatted = locale.format_string("%.1f", value, grouping=True)
    return value_formatted


def generate_unique_id():
    return uuid.uuid4()


def delete_folders(folder_name):
    """
    Deletes the specified file to ensure no unnecessary data is retained and to save storage space
    Uploaded file and folder containing files converted are deleted.

    :param folder_name: Contains the name/folder_id generated.
    :type folder_name: str
    :return: None
    :rtype: None

    PS: Keeping in print as platform doesn't allow access to local logs.
    """

    try:
        shutil.rmtree(upload_file_path(folder_name))
        print(f"Folder '{upload_file_path(folder_name)}' was deleted successfully.")
    except OSError as e:
        print(f"Error deleting folder '{folder_name}': {e}")

    time.sleep(60)
    try:
        shutil.rmtree(download_file_path(folder_name))
        print(f"Folder '{download_file_path(folder_name)}' was deleted successfully.")
    except OSError as e:
        print(f"Error deleting folder '{download_file_path(folder_name)}': {e}")
