import unittest

from markdown_service import block_to_block_type, markdown_to_blocks, BlockType, markdown_to_html_node
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
        block += "2. Internet. Connections can be via telephone line (DSL\*, digital subscriber line) or fiber optic cable (*Fiber optic*)."
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED)


    def test_markdown_to_html_node(self):
        with open("/home/a2100/workspace/github.com/alexskr96/static_site_generator/src/resources/Final Project Telecom.md", 'r') as file:
            markdown = file.read()

        html_node = markdown_to_html_node(markdown)
        target = ParentNode("div", [
            LeafNode("h1", "Final Project Telecom"),
            LeafNode("p", "---"),
            LeafNode("h1", "Telecom Task"),
            LeafNode("p", "The communication provider \"NoBreak\" wants to learn how to predict customer churn. If it is determined that a user intends to leave, they will be offered promotional codes and special offers. The operator's team has collected personal data on some customers, information about their tariffs, and contracts."),
            LeafNode("h3", "Service Description"),
            LeafNode("p", "The operator provides two main types of services:"),
            ParentNode("ol", [
                LeafNode("li", "Landline telephone service. It is possible to connect multiple phone lines simultaneously."),
                LeafNode("li", "Internet. Connections can be via telephone line (DSL, digital subscriber line) or fiber optic cable (*Fiber optic*).")
            ]),
            LeafNode("p", "Also available are the following services:"),
            ParentNode("ul", [
                LeafNode("li", "Internet security: antivirus (*DeviceProtection*) and blocking of unsafe websites (*OnlineSecurity*);"),
                LeafNode("li", "Dedicated support line (*TechSupport*);"),
                LeafNode("li", "Cloud file storage for data backup (*OnlineBackup*);"),
                LeafNode("li", "Streaming television (*StreamingTV*) and movie catalog (*StreamingMovies*).")
            ]),
            LeafNode("p", "Subscriptions can be paid monthly or through a contract lasting 1 to 2 years. Various payment methods are available, including the option to receive an electronic receipt."),
            LeafNode("h3", "Data Description"),
            LeafNode("p", "The data consists of files obtained from different sources:"),
            ParentNode("ul", [
                LeafNode("li", "contract.csv — information on contracts;"),
                LeafNode("li", "personal.csv — customer personal data;"),
                LeafNode("li", "internet.csv — internet service information;"),
                LeafNode("li", "phone.csv — telephone service information."),
            ]),
            LeafNode("p", "In all files, the column `customerID` contains the customer code."),
            LeafNode("p", "Information about contracts is current as of February 1, 2020."),
            LeafNode("h3", "Data"),
            LeafNode("p", "[final_provider.zip](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ac39c23b-718e-4cd6-bdaa-85b3a127a457/final_provider.zip)"),
            LeafNode("p", "The data is also located in the trainer, in the `/datasets/final_provider` directory.")
        ])
        html_node_children = html_node.get_children()
        target_children = target.get_children()

        for i in range(0, len(html_node_children)):
            self.assertEqual(html_node_children[i], target_children[i])
        self.assertEqual(html_node, target)
