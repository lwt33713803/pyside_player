import os


def load_stylesheet(filepath):
    with open(filepath, "r") as file:
        return file.read()


def load_assets(filepath):
    with open(filepath, "r") as file:
        return file.read()


def get_assets_path():
    current_path = os.getcwd()
    return os.path.join(current_path, 'assets')
