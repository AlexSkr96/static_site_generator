import unittest

from leafnode import LeafNode
from text_node_service import extract_markdown_links, extract_markdown_images, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_node_to_html_node, text_to_textnodes
from textnode import TextNode, TextType


class TestText(unittest.TestCase):
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

        text = "![final_provider.zip](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ac39c23b-718e-4cd6-bdaa-85b3a127a457/final_provider.zip)"
        images = extract_markdown_images(text)
        target = [("final_provider.zip", "https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ac39c23b-718e-4cd6-bdaa-85b3a127a457/final_provider.zip")]
        self.assertEqual(images, target)


    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        target = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(links, target)

        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        links = extract_markdown_links(text)
        target = []
        self.assertEqual(links, target)

        text = "[final_provider.zip](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ac39c23b-718e-4cd6-bdaa-85b3a127a457/final_provider.zip)"
        links = extract_markdown_links(text)
        target = [("final_provider.zip", "https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ac39c23b-718e-4cd6-bdaa-85b3a127a457/final_provider.zip")]
        self.assertEqual(links, target)


    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        target = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(new_nodes, target)

        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        target = [
            TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(new_nodes, target)

        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        target = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, target)


    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        target = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(new_nodes, target)


        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        target = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and ", TextType.TEXT),
            TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(new_nodes, target)


        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        target = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, target)


    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        target = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, target)


        text = "**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)"
        nodes = text_to_textnodes(text)
        target = [
            TextNode("I like Tolkien", TextType.BOLD),
            TextNode(". Read my ", TextType.TEXT),
            TextNode("first post here", TextType.LINK, "/majesty"),
            TextNode(" (sorry the link doesn't work yet)", TextType.TEXT)
        ]
        self.assertEqual(nodes, target)
