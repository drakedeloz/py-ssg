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
