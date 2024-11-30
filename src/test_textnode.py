import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node = TextNode("This is a text node", TextType.BOLD, "https://github.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://github.com")
        self.assertEqual(node, node2)
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://github.com")
        self.assertNotEqual(node, node2)
        node = TextNode("This is a text node", TextType.BOLD, "github.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://github.com")
        self.assertNotEqual(node, node2)
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()