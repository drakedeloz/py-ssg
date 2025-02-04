import unittest

from inline import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(nodes) == 3

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("This **bold** and **more bold**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(nodes) == 4
        # What assertions would verify the correct splitting?

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("Plain text without delimiter", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        assert len(nodes) == 1
        assert nodes[0] == TextNode("Plain text without delimiter", TextType.TEXT)

    def test_split_nodes_delimiter_already_processed(self):
        node = TextNode("Already bold", TextType.BOLD)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(nodes) == 1

    def test_split_nodes_delimiter_unclosed(self):
        with self.assertRaises(Exception):
            node = TextNode("This `code is unclosed", TextType.TEXT)
            nodes = split_nodes_delimiter([node], "`", TextType.CODE)
