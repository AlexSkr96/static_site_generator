import unittest

from markdown_service import block_to_block_type, markdown_to_blocks, BlockType

class TestMarkdownService(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
    # Heading 1

    # Heading 2

    This is a paragraph.
    """

        blocks = markdown_to_blocks(markdown)
        target = [
            "# Heading 1\n",
            "# Heading 2\n",
            "This is a paragraph.\n"
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
            "# This is a heading\n",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n",
            "* This is the first list item in a list block\n" +
                "* This is a list item\n" +
                "* This is another list item\n"
        ]
        self.assertEqual(blocks, target)


    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# This is a heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Another Level of Heading"), BlockType.HEADING)

        self.assertEqual(block_to_block_type("```python\nprint('Hello, world!')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```python print('Hello, world!') ```"), BlockType.CODE)

        block = "> This is a quoted line\n> And another one"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERD)

        block = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERD)

        self.assertEqual(block_to_block_type("This is a normal piece of text"), BlockType.TEXT)
        self.assertEqual(block_to_block_type("* This is an item in an unordered list *"), BlockType.UNORDERD)
