import os
import shutil

from directory_service import copy_dir_contents, generate_page


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")

    copy_dir_contents("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
