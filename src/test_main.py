import unittest

from leafnode import LeafNode
from main import extract_markdown_links, extract_markdown_images, split_nodes_delimiter, text_node_to_html_node
from textnode import TextNode, TextType


class TestMain(unittest.TestCase):
    def test_text_node_to_html_node(self):
        text_node = TextNode(text="text", text_type=TextType.TEXT)
        test_html_node = text_node_to_html_node(text_node)
        target_html_node = LeafNode(value="text", tag=None)
        self.assertEqual(test_html_node, target_html_node)

        text_node = TextNode(text="bold", text_type=TextType.BOLD)
        test_html_node = text_node_to_html_node(text_node)
        target_html_node = LeafNode(value="bold", tag="b")
        self.assertEqual(test_html_node, target_html_node)

        text_node = TextNode(text="italic", text_type=TextType.ITALIC)
        test_html_node = text_node_to_html_node(text_node)
        target_html_node = LeafNode(value="italic", tag="i")
        self.assertEqual(test_html_node, target_html_node)

        text_node = TextNode(text="print(\"hello world\")", text_type=TextType.CODE)
        test_html_node = text_node_to_html_node(text_node)
        target_html_node = LeafNode(value="print(\"hello world\")", tag="code")
        self.assertEqual(test_html_node, target_html_node)

        text_node = TextNode(text="DuckDuckGo", text_type=TextType.LINK, url="https://duckduckgo.com")
        test_html_node = text_node_to_html_node(text_node)
        target_html_node = LeafNode(value="DuckDuckGo", tag="a", props={"href": text_node.get_url()})
        self.assertEqual(test_html_node, target_html_node)

        text_node = TextNode(text="Swedish flag", text_type=TextType.IMAGE, url = "https://flagsweb.com/images/PNG/Flag_of_Sweden.png")
        test_html_node = text_node_to_html_node(text_node)
        target_html_node = LeafNode(value="", tag="img", props={
            "src": "https://flagsweb.com/images/PNG/Flag_of_Sweden.png",
            "alt": "Swedish flag"
        })
        self.assertEqual(test_html_node, target_html_node)


    def test_split_nodes_delimiter(self):
        italic_node = TextNode("This is text *italic*, some more text", TextType.TEXT)
        result = split_nodes_delimiter([italic_node], "*", TextType.ITALIC)
        target = [
            TextNode("This is text ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", some more text", TextType.TEXT)
        ]
        self.assertEqual(result, target)

        # italic_node = TextNode("This is text \*italic*, some more text", TextType.TEXT)
        # result = split_nodes_delimiter([italic_node], "*", TextType.ITALIC)
        # target = [
        #     TextNode("This is text \*italic", TextType.TEXT),
        #     TextNode(", some more text", TextType.ITALIC)
        # ]
        # self.assertEqual(result, target)

        italic_node = TextNode("*italic*, This is text, some more text", TextType.TEXT)
        result = split_nodes_delimiter([italic_node], "*", TextType.ITALIC)
        target = [
            TextNode("italic", TextType.ITALIC),
            TextNode(", This is text, some more text", TextType.TEXT)
        ]
        self.assertEqual(result, target)

        bold_node = TextNode("This is text **bold**, some more text", TextType.TEXT)
        result = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        target = [
            TextNode("This is text ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", some more text", TextType.TEXT)
        ]
        self.assertEqual(result, target)


    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        target = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(images, target)

        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        images = extract_markdown_images(text)
        target = []
        self.assertEqual(images, target)


    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        images = extract_markdown_links(text)
        target = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(images, target)

        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_links(text)
        target = []
        self.assertEqual(images, target)
