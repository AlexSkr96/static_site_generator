import re
from textnode import TextNode, TextType
from leafnode import LeafNode


def main():
    pass


def text_node_to_html_node(text_node):
    match text_node.get_text_type().value:
        case "text":
            return LeafNode(value=text_node.get_text(), tag=None)
        case "bold":
            return LeafNode(value=text_node.get_text(), tag="b")
        case "italic":
            return LeafNode(value=text_node.get_text(), tag="i")
        case "code":
            return LeafNode(value=text_node.get_text(), tag="code")
        case "link":
            return LeafNode(value=text_node.get_text(), tag="a", props={"href": text_node.get_url()})
        case "image":
            return LeafNode(value="", tag="img", props={"src": text_node.get_url(), "alt": text_node.get_text()})
        case _:
            raise ValueError("Invalid text type!")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for node in old_nodes:
        if node.get_text_type() != TextType.TEXT:
            res.append(node)
            continue

        text = node.get_text() + delimiter
        node_start = 0
        new_text_type = text_type
        delimiter_ind = 0

        while delimiter_ind != -1:
            delimiter_ind = text.find(delimiter, node_start)
            node_text = text[node_start:delimiter_ind]
            node_start = delimiter_ind + len(delimiter)
            new_text_type = text_type if new_text_type != text_type else node.get_text_type()
            if len(node_text) == 0:
                continue

            res.append(TextNode(node_text, new_text_type))

    return res


def extract_markdown_images(text):
    res = []
    pattern = r"!\[[^\]]*?\]\(https?:\/\/.*?\)"
    image_links = re.findall(pattern, text)
    for link in image_links:
        link_elements = link[2:-1].split("](")
        alt_text = link_elements[0]
        link = link_elements[1]
        res.append((alt_text, link))

    return res


def extract_markdown_links(text):
    res = []
    pattern = r"[^!]\[[^\]]*?\]\(https?:\/\/.*?\)"
    # '" " + text' in case it starts with a link
    image_links = re.findall(pattern, " " + text)
    for link in image_links:
        link_elements = link[2:-1].split("](")
        alt_text = link_elements[0]
        link = link_elements[1]
        res.append((alt_text, link))

    return res


def split_nodes_image(old_nodes):
    res = []
    for node in old_nodes:
        text = node.get_text()
        image_links = extract_markdown_images(node.get_text())
        if not image_links:
            res.append(node)
            continue

        for link in image_links:
            link_text = f"![{link[0]}]({link[1]})"
            text_split = text.split(link_text)
            res.append(TextNode(text_split[0], TextType.TEXT))
            res.append(TextNode(link[0], TextType.IMAGE, link[1]))
            text = text_split[1]

        if len(text) > 0:
            res.append(TextNode(text, TextType.TEXT))

    return res


def split_nodes_link(old_nodes):
    res = []
    for node in old_nodes:
        text = node.get_text()
        links = extract_markdown_links(node.get_text())
        if not links:
            res.append(node)
            continue

        for link in links:
            link_text = f"[{link[0]}]({link[1]})"
            text_split = text.split(link_text)

            if text_split[0][-1] == "!":
                if links[-1] == link:
                    res.append(TextNode(text, TextType.TEXT))
                else:
                    continue
            else:
                res.append(TextNode(text_split[0], TextType.TEXT))
                res.append(TextNode(link[0], TextType.LINK, link[1]))
                text = text_split[1]

        if len(text) > 0:
            res.append(TextNode(text, TextType.TEXT))

    return res


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    return nodes


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



if __name__ == "__main__":
    main()
