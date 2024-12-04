from textnode import TextNode, TextType
from leafnode import LeafNode


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)


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
        text = node.get_text() + delimiter
        node_start = 0
        new_text_type = text_type
        delimiter_ind = 0

        while delimiter_ind != -1:
            delimiter_ind = text.find(delimiter, node_start)
            node_text = text[node_start:delimiter_ind]
            node_start = delimiter_ind + len(delimiter)
            new_text_type = text_type if new_text_type != text_type else TextType.TEXT
            if len(node_text) == 0:
                continue

            res.append(TextNode(node_text, new_text_type))

    return res


if __name__ == "__main__":
    main()
