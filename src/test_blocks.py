import unittest
from blocks import *

class TestBlocks(unittest.TestCase):
    def test_blocks(self):
        text = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item
        """
        result = markdown_to_blocks(text)
        assert result == ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.','* This is the first list item in a list block\n        * This is a list item\n        * This is another list item']


    def test_markdown_to_blocks(self):
        test_input = "Block 1\n\n\n   Block 2   \n\n\nBlock 3"
        result = markdown_to_blocks(test_input)
        assert result == ["Block 1", "Block 2", "Block 3"]

        test_input = "Block 1\n\n    \n\nBlock 2"
        result = markdown_to_blocks(test_input)
        assert result == ["Block 1", "Block 2"]

    def test_markdown_to_blocks(self):
        test_input = """Here's some code:

        def hello():
            print('Hello')
            print('World')

        This is another block"""
        
        result = markdown_to_blocks(test_input)
        expected = [
            "Here's some code:",
            "def hello():\n            print('Hello')\n            print('World')",
            "This is another block"
        ]
        assert result == expected
