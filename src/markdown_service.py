from enum import Enum
import re

from parentnode import ParentNode
from leafnode import LeafNode
from xml.dom import NotFoundErr

from text_node_service import text_node_to_html_node, text_to_textnodes


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

        html_block_nodes = None
        if block_type == BlockType.HEADING:
            heading_level = 0
            for char in block:
                if char == "#":
                    heading_level += 1
                else:
                    break

            tag = f"h{heading_level}"
            node_text = block.lstrip("#").strip()
            text_nodes = text_to_textnodes(node_text)
            html_block_nodes = list(map(text_node_to_html_node, text_nodes))

        elif block_type == BlockType.CODE:
            tag = "code"
            node_text = block.strip("`")
            text_nodes = text_to_textnodes(node_text)
            html_block_nodes = list(map(text_node_to_html_node, text_nodes))

        elif block_type == BlockType.TEXT:
            tag = "p"
            node_text = block
            text_nodes = text_to_textnodes(node_text)
            html_block_nodes = list(map(text_node_to_html_node, text_nodes))

        elif block_type == BlockType.QUOTE:
            tag = "blockqoute"
            for line in block.split("\n"):
                node_text += f"{line[2:]}\n"

            text_nodes = text_to_textnodes(node_text)
            html_block_nodes = list(map(text_node_to_html_node, text_nodes))

        elif block_type == BlockType.ORDERED:
            html_block_nodes = []
            for line in block.split("\n"):
                node_text = line[3:].strip()
                text_nodes = text_to_textnodes(node_text)
                html_line_node = list(map(text_node_to_html_node, text_nodes))
                html_block_nodes.append(ParentNode("li", html_line_node))

            tag = "ol"

        elif block_type == BlockType.UNORDERED:
            html_block_nodes = []
            for line in block.split("\n"):
                node_text = line[2:].strip()
                text_nodes = text_to_textnodes(node_text)
                html_line_node = list(map(text_node_to_html_node, text_nodes))
                html_block_nodes.append(ParentNode("li", html_line_node))

            tag = "ul"

        if tag:
            new_node = ParentNode(tag, html_block_nodes)
            html_nodes.append(new_node)

    parent_node = ParentNode("div", html_nodes)
    return parent_node


def extract_title(markdown):
    match = re.search(r"^\s*# .+", markdown, re.M)
    if match:
        title = match.group()
        return title[2:].strip()
    else:
        raise NotFoundErr("Title not found")
