import os
import shutil

from markdown_service import extract_title, markdown_to_html_node
import re


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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = ""
    with open(from_path) as file:
        markdown = file.read()

    template = ""
    with open(template_path) as file:
        template = file.read()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok = True)
    with open(dest_path, 'w') as file:
        file.write(template)
