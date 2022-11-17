import subprocess
import os
from contextlib import contextmanager

@contextmanager
def working_dir(directory):
    original_working_dir = os.getcwd()
    try:
        os.chdir(directory)
        yield directory
    finally:
        os.chdir(original_working_dir)


def find_matching_files_in_dir(file_prefix: str, directory: str) -> list:
    files = [
        directory + '/' + filename
        for filename in os.listdir(directory)
        if filename.startswith(file_prefix) and filename.endswith('.png')
    ]
    return files


def get_images(pdf_filepath: str, type: str) -> list:
    directory, filename = os.path.split(pdf_filepath)
    if type == 'mir':
        res = '600'
    else:
        res = '300'
    with working_dir(directory):
        subprocess.run(["pdftocairo", "-png", "-r", res, filename, filename.split(".pdf")[0]])
    return find_matching_files_in_dir(filename.split(".pdf")[0], directory)
