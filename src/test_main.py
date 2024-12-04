import unittest

from leafnode import LeafNode
from main import text_node_to_html_node
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
