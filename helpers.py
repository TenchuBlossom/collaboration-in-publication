import os

def make_dir(dir_chain: list):
    destination_dir = './'
    for folder in dir_chain:
        destination_dir = os.path.join(destination_dir, folder)
        if not os.path.isdir(destination_dir):
            os.mkdir(destination_dir)

    return destination_dir