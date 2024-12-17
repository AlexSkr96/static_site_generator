import os
import shutil


def copy_dir_contents(source, destination):
    if not os.path.exists(source):
        raise FileNotFoundError(f"{source} doesn't exist")
    elif not os.path.isdir(source):
        raise NotADirectoryError(f"{source} is not a directory")

    if not os.path.exists(destination):
        os.mkdir(destination)

    for el in os.listdir(source):
        sub_source = os.path.join(source, el)
        sub_destination = os.path.join(destination, el)
        if os.path.isfile(sub_source):
            print(f"Copy from {sub_source} to {sub_destination}")
            shutil.copy(sub_source, sub_destination)
        else:
            copy_dir_contents(sub_source, sub_destination)
