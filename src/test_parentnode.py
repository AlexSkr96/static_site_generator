import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        with self.assertRaises(ValueError):
            test_node = ParentNode(tag="", children=[])
            test_node.to_html()

        with self.assertRaises(ValueError):
            test_node = ParentNode(tag="p", children=[])
            test_node.to_html()

        leaf_node1 = LeafNode(tag="d", value="Child_node1")
        test_node = ParentNode(tag="p", children=[leaf_node1])
        self.assertEqual(test_node.to_html(), "<p><d>Child_node1</d></p>")

        leaf_node2 = LeafNode(tag="d", value="Child link node", props={"href": "https://duckduckgo.com"})
        sub_parent_node = ParentNode(tag="d", children=[leaf_node2])
        test_node = ParentNode(tag="p", children=[leaf_node1, sub_parent_node])
        self.assertEqual(test_node.to_html(), "<p><d>Child_node1</d><d><d href=https://duckduckgo.com>Child link node</d></d></p>")

        test_node = ParentNode(tag="p", children=[leaf_node1, sub_parent_node])
        print(test_node.to_html())
        target_html = "<p>\n"
        target_html += "\t<d>Child_node1</d>\n"
        target_html += "\t<d>\n"
        target_html += "\t\t<d href=https://duckduckgo.com>Child link node</d>\n"
        target_html += "\t</d>\n"
        target_html += "</p>"
        self.assertEqual(test_node.to_html(pretty=True), target_html)
