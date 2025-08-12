import os
import shutil
import sys

from copystatic import copy_files
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
from_path = "./content"
template_path = "./template.html"
dest_path = "./public"

def main():
    print("Deleting public directory...")

    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("base path: " + basepath)

    print("Copying static files to public directory...")
    copy_files(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_pages_recursive(from_path, template_path, dir_path_public, basepath)

main()