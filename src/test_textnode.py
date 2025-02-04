import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://thisisaurl.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://thisisaurl.com")
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("this is not a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_not_eq3(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://thisisaurl.com")
        node2 = TextNode("This is a text node", TextType.IMAGE, "https://thisisnotaurl.com")
        self.assertNotEqual(node, node2)
    
    def test_text_node_to_html_node(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == None
        assert html_node.value == "Hello, world!"
        assert html_node.props == None
