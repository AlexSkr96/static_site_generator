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


if __name__ == "__main__":
    main()
