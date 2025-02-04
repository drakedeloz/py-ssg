from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    regex_delim = delimiter
    match delimiter:
        case "**":
            regex_delim = "\\*\\*"
        case "*":
            regex_delim = "\\*"
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        split_text = re.split(f"({regex_delim})", node.text)
        opened = False
        classified_strings = []
        for item in split_text:
            if delimiter in item and not opened:
                opened = True
                continue
            elif delimiter in item and opened:
                opened = False
                continue

            if opened:
                classified_strings.append((item, text_type))
            else:
                classified_strings.append((item, TextType.TEXT))
        if opened:
            raise Exception("invalid markdown")
        for key, val in classified_strings:
            results.append(TextNode(str(key), val))
    return results
