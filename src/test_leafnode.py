import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode('p', 'Lorem ipsum')
        self.assertEqual(node.to_html(), "<p>Lorem ipsum</p>")

        node = LeafNode('p', 'boot.dev', {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), "<p href=https://boot.dev>boot.dev</p>")
