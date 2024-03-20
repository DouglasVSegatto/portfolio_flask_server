import locale
import os

"""
Created this 'global_functions' as few can be reused many times by other apps.
"""

def remove_extension(filename):
    """
    Remove the file extension from the given filename and return the main name.

    :param filename: Contains original filename uploaded, including its extension.
    :type filename: str
    :return: The main filename without the extension.
    :rtype: str
    """
    return os.path.splitext(filename)[0]


def upload_file_path(filename):
    """
    Creates os path for upload folder with filename, including its extension

    :param filename: Contains original filename uploaded, including its extension.
    :type filename: str
    :return: Path to uploaded file
    :rtype: str
    """
    return os.path.join("static", "upload", filename)


def download_file_path(filename):
    """
    Creates os path for download folder with filename:
        Tracking folder - filename must be passed without its extension.
        Tracking file - filename must be passed including its extension.

    :param filename: Contains original filename uploaded, including/excluding its extension.
    :type filename: str
    :return: Path to download file/folder
    :rtype: str
    """
    return os.path.join("static", "download", filename)


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
