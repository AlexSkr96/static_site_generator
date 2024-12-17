import os
import shutil

from directory_service import copy_dir_contents


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")

    copy_dir_contents("static", "public")


if __name__ == "__main__":
    main()
