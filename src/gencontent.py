import os
from markdown_blocks import markdown_to_html_node, markdown_to_blocks


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    
    raise Exception("No h1 header")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = ""
    template = ""

    try:
        with open(from_path, 'r') as file:
            markdown = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file {from_path} was not found.")
    except Exception as e:
        raise e

    try:
        with open(template_path, 'r') as file:
            template = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file {template_path} was not found.")
    except Exception as e:
        raise e
    
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}').replace('src="/', f'href="{basepath}')

    dest_dir_name = os.path.dirname(dest_path)

    if not os.path.exists(dest_dir_name):
        os.makedirs(dest_dir_name, exist_ok=True)

    try:
        with open(dest_path, 'w') as file:
            file.write(template)
    except Exception as e:
        raise e
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dir_path_content) or not os.path.isdir(dir_path_content):
        raise Exception("Error: source path doesn't exist, or is not a directory")
    
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)
    
    if not os.path.isdir(dest_dir_path):
        raise Exception("Error: destination path is not a directory")
    
    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        destination_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_path):
            if not source_path.endswith(".md"):
                continue

            root, ext = os.path.splitext(destination_path)

            generate_page(source_path, template_path, root + ".html", basepath)
        else:
            generate_pages_recursive(source_path, template_path, destination_path, basepath)