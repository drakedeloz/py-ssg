from textnode import *
import re

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for node in old_nodes:
        split_nodes = []
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            results.extend(split_nodes)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("Invalid markdown")
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_text[i], text_type))
        results.extend(split_nodes)
    return results

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        text = node.text
        if not text:
            continue
        split_nodes = []
        images = extract_markdown_images(text)
        if not images:
            split_nodes.append(node)
        else:
            remaining_text = text
            for image in images:
                delimiter = f"![{image[0]}]({image[1]})"
                sections = remaining_text.split(delimiter, 1)
                if sections[0]:
                    split_nodes.append(TextNode(sections[0], TextType.TEXT))
                split_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                if len(sections) > 1:
                    remaining_text = sections[1]
                else:
                    remaining_text = ""
            if remaining_text:
                split_nodes.append(TextNode(remaining_text, TextType.TEXT))
        result.extend(split_nodes)
    return result

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_links(old_nodes):
    result = []
    for node in old_nodes:
        text = node.text
        if not text:
            continue
        split_nodes = []
        links = extract_markdown_links(text)
        if not links:
            split_nodes.append(node)
        else:
            remaining_text = text
            for link in links:
                delimiter = f"[{link[0]}]({link[1]})"
                sections = remaining_text.split(delimiter, 1)
                if sections[0]:
                    split_nodes.append(TextNode(sections[0], TextType.TEXT))
                split_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                if len(sections) > 1:
                    remaining_text = sections[1]
                else:
                    remaining_text = ""
            if remaining_text:
                split_nodes.append(TextNode(remaining_text, TextType.TEXT))
        result.extend(split_nodes)
    return result

