from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        split_nodes = []
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

#def extract_markdown_images(text):
    
