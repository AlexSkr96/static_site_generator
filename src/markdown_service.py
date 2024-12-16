from enum import Enum
import re

from parentnode import ParentNode
from leafnode import LeafNode


class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    TEXT = "text"
    QUOTE = "quote"
    ORDERED = "ordered"
    UNORDERED = "unordered"



def markdown_to_blocks(markdown):
    blocks = []
    markdown_list = markdown.strip().split("\n") + [""]
    block = ""
    for row in markdown_list:
        row = row.strip()
        if len(row) > 0:
            block += f"{row}\n"
        elif len(block) > 0:
            blocks.append(block.strip())
            block = ""

    return blocks


def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r"^```(.|\n)*```$", block) and "```" not in block[3:-3]:
        return BlockType.CODE
    elif re.match(r"^>", block):
        for line in block.strip().split("\n")[1:]:
            if not re.match(r"^>", line):
                return BlockType.TEXT

        return BlockType.QUOTE
    elif re.match(r"^[\*-] ", block):
        for line in block.strip().split("\n")[1:]:
            if not re.match(r"^[\*-] ", line):
                return BlockType.TEXT

        return BlockType.UNORDERED
    elif re.match(r"^[0-9]\. ", block):
        for line in block.strip().split("\n")[1:]:
            if not re.match(r"^[0-9]\. ", line):
                return BlockType.TEXT

        return BlockType.ORDERED
    else:
        return BlockType.TEXT


def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block = block.strip()
        tag = ""
        node_text = ""
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            heading_level = 0
            for char in block:
                if char == "#":
                    heading_level += 1
                else:
                    break

            tag = f"h{heading_level}"
            node_text = block.lstrip("#")

        elif block_type == BlockType.CODE:
            tag = "code"
            node_text = block.strip("`")

        elif block_type == BlockType.TEXT:
            tag = "p"
            node_text = block

        elif block_type == BlockType.QUOTE:
            tag = "blockqoute"
            for line in block.split("\n"):
                node_text += f"{line[2:]}\n"

        elif block_type == BlockType.ORDERED:
            ordered_nodes = []
            for line in block.split("\n"):
                ordered_nodes.append(LeafNode("li", line[3:].strip()))

            new_node = ParentNode("ol", ordered_nodes)
            html_nodes.append(new_node)

        elif block_type == BlockType.UNORDERED:
            unordered_nodes = []
            for line in block.split("\n"):
                unordered_nodes.append(LeafNode("li", line[2:].strip()))

            new_node = ParentNode("ul", unordered_nodes)
            html_nodes.append(new_node)

        if tag:
            new_node = LeafNode(tag, node_text.strip())
            html_nodes.append(new_node)

    parent_node = ParentNode("div", html_nodes)
    return parent_node
