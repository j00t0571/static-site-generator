import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        old_text_type = old_node.text_type

        if old_text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        for i in range(len(split_text)):
            if split_text[i] == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], old_text_type))
            else:
                new_nodes.append(TextNode(split_text[i], text_type))
        
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        old_node_text = old_node.text
        images = extract_markdown_images(old_node_text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            split_text = old_node_text.split(f"![{image[0]}]({image[1]})", 1)

            if len(split_text) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))

            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )

            old_node_text = split_text[1]

        if old_node_text != "":
            new_nodes.append(TextNode(old_node_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        old_node_text = old_node.text
        old_node_links = extract_markdown_links(old_node_text)

        if len(old_node_links) == 0:
            new_nodes.append(old_node)
            continue

        for link in old_node_links:
            split_text = old_node_text.split(f"[{link[0]}]({link[1]})", 1)

            if len(split_text) != 2:
                raise ValueError("invalid markdown, link section not closed")
            
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))

            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            old_node_text = split_text[1]

        if old_node_text != "":
            new_nodes.append(TextNode(old_node_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes