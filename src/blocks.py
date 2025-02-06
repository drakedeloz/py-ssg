import re

def markdown_to_blocks(markdown):
    text = markdown
    blocks = re.split("\n\n", text)
    valid_blocks = []
    for block in blocks:
        item = block.strip()
        if item:
            valid_blocks.append(item)
    return valid_blocks

def block_to_block_type(markdown_block):
    if markdown_block.startswith("#"):
        split = markdown_block.split()
        if all(char == "#" for char in split[0]) and len(split[0]) < 7:
            return "heading"

    if markdown_block.startswith("```"):
        if markdown_block.endswith("```"):
            return "code"

    if markdown_block.startswith(">"):
        split = markdown_block.split("\n")
        if all(line.startswith(">") for line in split):
            return "quote"

    if markdown_block.startswith("*"):
        split = markdown_block.split("\n")
        if all(line.startswith("* ") for line in split):
            return "unordered_list"

    if markdown_block.startswith("-"):
        split = markdown_block.split("\n")
        if all(line.startswith("- ") for line in split):
            return "unordered_list"

    if markdown_block.startswith("1."):
        split = markdown_block.split("\n")
        if all(split[i].startswith(f"{i}. ") for i in range(len(split))):
            return "ordered_list"
    return "paragraph"
