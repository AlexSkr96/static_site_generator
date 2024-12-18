import unittest

from markdown_service import extract_title, block_to_block_type, markdown_to_blocks, BlockType, markdown_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode


class TestMarkdownService(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
    # Heading 1

    # Heading 2

    This is a paragraph.
    """

        blocks = markdown_to_blocks(markdown)
        target = [
            "# Heading 1",
            "# Heading 2",
            "This is a paragraph."
        ]

        self.assertEqual(blocks, target)


        markdown = """
    # This is a heading

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    * This is the first list item in a list block
    * This is a list item
    * This is another list item"""

        blocks = markdown_to_blocks(markdown)
        target = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n" +
                "* This is a list item\n" +
                "* This is another list item"
        ]
        self.assertEqual(blocks, target)


    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# This is a heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Another Level of Heading"), BlockType.HEADING)

        self.assertEqual(block_to_block_type("```python\nprint('Hello, world!')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```python print('Hello, world!') ```"), BlockType.CODE)

        block = "> This is a quoted line\n> And another one"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED)

        block = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED)

        self.assertEqual(block_to_block_type("This is a normal piece of text"), BlockType.TEXT)
        self.assertEqual(block_to_block_type("* This is an item in an unordered list *"), BlockType.UNORDERED)

        block = "1. Landline telephone service. It is possible to connect multiple phone lines simultaneously.\n"
        block += "2. Internet. Connections can be via telephone line (DSL*, digital subscriber line) or fiber optic cable (*Fiber optic*)."
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED)


    def test_markdown_to_html_node(self):
        with open("/home/a2100/workspace/github.com/alexskr96/static_site_generator/src/resources/Final Project Telecom.md", 'r') as file:
            markdown = file.read()

        html_node = markdown_to_html_node(markdown)
        target = ParentNode("div", [
            ParentNode("h1", [LeafNode(value="Final Project Telecom")]),
            ParentNode("p", [LeafNode(value="---")]),
            ParentNode("h1", [LeafNode(value="Telecom Task")]),
            ParentNode("p", [LeafNode(value="The communication provider \"NoBreak\" wants to learn how to predict customer churn. If it is determined that a user intends to leave, they will be offered promotional codes and special offers. The operator's team has collected personal data on some customers, information about their tariffs, and contracts.")]),
            ParentNode("h3", [LeafNode(value="Service Description")]),
            ParentNode("p", [LeafNode(value="The operator provides two main types of services:")]),
            ParentNode("ol", [
                ParentNode("li", [LeafNode(value="Landline telephone service. It is possible to connect multiple phone lines simultaneously.")]),
                ParentNode("li", [
                    LeafNode(value="Internet. Connections can be via telephone line (DSL, digital subscriber line) or fiber optic cable ("),
                    LeafNode(tag="i", value="Fiber optic"),
                    LeafNode(value=").")
                ])
            ]),
            ParentNode("p", [LeafNode(value="Also available are the following services:")]),
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode(value="Internet security: antivirus ("),
                    LeafNode(tag="i", value="DeviceProtection"),
                    LeafNode(value=") and blocking of unsafe websites ("),
                    LeafNode(tag="i", value="OnlineSecurity"),
                    LeafNode(value=");")
                ]),
                ParentNode("li", [
                    LeafNode(value="Dedicated support line ("),
                    LeafNode(tag="i", value="TechSupport"),
                    LeafNode(value=");")
                ]),
                ParentNode("li", [
                    LeafNode(value="Cloud file storage for data backup ("),
                    LeafNode(tag="i", value="OnlineBackup"),
                    LeafNode(value=");")
                ]),
                ParentNode("li", [
                    LeafNode(value="Streaming television ("),
                    LeafNode(tag="i", value="StreamingTV"),
                    LeafNode(value=") and movie catalog ("),
                    LeafNode(tag="i", value="StreamingMovies"),
                    LeafNode(value=").")
                ])
            ]),
            ParentNode("p", LeafNode(value="Subscriptions can be paid monthly or through a contract lasting 1 to 2 years. Various payment methods are available, including the option to receive an electronic receipt.")),
            ParentNode("h3", LeafNode(value="Data Description")),
            ParentNode("p", LeafNode(value="The data consists of files obtained from different sources:")),
            ParentNode("ul", [
                ParentNode("li", LeafNode(value="contract.csv — information on contracts;")),
                ParentNode("li", LeafNode(value="personal.csv — customer personal data;")),
                ParentNode("li", LeafNode(value="internet.csv — internet service information;")),
                ParentNode("li", LeafNode(value="phone.csv — telephone service information.")),
            ]),
            ParentNode("p", [
                LeafNode(value="In all files, the column "),
                LeafNode(tag="code", value="customerID"),
                LeafNode(value=" contains the customer code.")
            ]),
            ParentNode("p", LeafNode(value="Information about contracts is current as of February 1, 2020.")),
            ParentNode("h3", LeafNode(value="Data")),
            ParentNode("p", LeafNode(
                tag = "a",
                value="final_provider.zip",
                props={"href": "https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ac39c23b-718e-4cd6-bdaa-85b3a127a457/final_provider.zip"}
            )),
            ParentNode("p", [
                LeafNode(value="The data is also located in the trainer, in the "),
                LeafNode(tag="code", value="/datasets/final_provider"),
                LeafNode(value=" directory.")
            ])
        ])

        def assertEqualEach(node1, node2):
            if node1.get_children() and node2.get_children():
                node1_children = node1.get_children()
                node2_children = node2.get_children()
                for i in range(0, min(len(node1_children), len(node2_children))):
                    assertEqualEach(node1_children[i], node2_children[i])

            self.assertEqual(node1, node2)

        assertEqualEach(html_node, target)



    def test_extract_title(self):
        with open("/home/a2100/workspace/github.com/alexskr96/static_site_generator/src/resources/Final Project Telecom.md", 'r') as file:
            markdown = file.read()

        title = extract_title(markdown)
        target = "Final Project Telecom"
        self.assertEqual(title, target)


        markdown = "something\n# Title"
        title = extract_title(markdown)
        target = "Title"
        self.assertEqual(title, target)
