import os

def get_root_directory():
    return os.getcwd()

def full_root_path(file):
    folder = get_root_directory()
    return os.path.join(folder, file)

def get_directory():
    return os.path.dirname(os.path.abspath(__file__))

def full_path(file):
    folder = get_directory()
    return os.path.join(folder, file)
