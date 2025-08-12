import os
import shutil
from htmlnode import HTMLNode, LeafNode, ParentNode

def copy_files(source, destination):
    if not os.path.exists(source) or not os.path.isdir(source):
        raise Exception("Error: source path doesn't exist, or is not a directory")
    
    if not os.path.exists(destination):
        os.mkdir(destination)
    
    if not os.path.isdir(destination):
        raise Exception("Error: destination path is not a directory")
    
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        print(f'{source_path} -> {destination_path}')

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        else:
            copy_files(source_path, destination_path)