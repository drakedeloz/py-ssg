from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("Invalid markdown")
        for i in range(len(split_text)):
            if i % 2 == 0:
                results.append(TextNode(split_text[i], TextType.TEXT))
            else:
                results.append(TextNode(split_text[i], text_type))
    return results
