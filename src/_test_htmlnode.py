import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node2 = HTMLNode(
            "p",
            "Test text"
        )
        node3 = HTMLNode(
            "h1",
            "Hey there"
        )
        node = HTMLNode(
            "p",
            "Lorem ipsum",
            [node2, node3],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        expected = """HTMLNode(<p>, Lorem ipsum, 2 children,\n {'href': 'https://www.google.com', 'target': '_blank'})"""
        self.assertEqual(repr(node), expected)



    def test_props_to_html(self):
        pass



    if __name__ == "__main__":
        unittest.main()
