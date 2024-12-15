from enum import Enum
import re


class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    TEXT = "text"
    QUOTE = "quote"
    ORDERD = "orderd"
    UNORDERD = "unorderd"



def markdown_to_blocks(markdown):
    blocks = []
    markdown_list = markdown.strip().split("\n") + [""]
    block = ""
    for row in markdown_list:
        row = row.strip()
        if len(row) > 0:
            block += f"{row}\n"
        elif len(block) > 0:
            blocks.append(block)
            block = ""

    return blocks


def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r"^```(.|\n)*```$", block) and "```" not in block[3:-3]:
        return BlockType.CODE
    elif re.match(r"^>", block):
        for line in block.split("\n")[1:]:
            if not re.match(r"^>", line):
                return BlockType.TEXT

        return BlockType.QUOTE
    elif re.match(r"^[\*-] ", block):
        for line in block.split("\n")[1:]:
            if not re.match(r"^[\*-] ", line):
                return BlockType.TEXT

        return BlockType.UNORDERD
    elif re.match(r"^[0-9]\. ", block):
        for line in block.split("\n")[1:]:
            if not re.match(r"^[0-9]\. ", line):
                return BlockType.TEXT

        return BlockType.ORDERD
    else:
        return BlockType.TEXT


# def markdown_to_html_node(markdown):
#     blocks = markdown_to_blocks(markdown)
#     for block in blocks:
