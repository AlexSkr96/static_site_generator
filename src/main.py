import os
import shutil

from directory_service import copy_dir_contents, generate_pages_recursive


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")

    copy_dir_contents("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
