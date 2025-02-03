import unittest

from htmlnode import HTMLNode, HTMLType, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            HTMLType.PARAGRAPH, 
            "This is a paragraph of text", 
            None, 
            {"styles": "font-family:Garamond;color:red;"}
        )
        self.assertEqual(
            node.props_to_html(), 
            ' styles="font-family:Garamond;color:red;"'
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode(HTMLType.heading(1), "This is a heading")
        self.assertIsNone(node.props_to_html())

    def test_repr(self):
        node = HTMLNode(
            HTMLType.heading(2), 
            "This is a heading", 
            None, 
            {"styles": "font-family:Times;color:blue"}
        )
        expected = 'HTMLNode(h2, This is a heading, None, {\'styles\': \'font-family:Times;color:blue\'})'
        self.assertEqual(str(node), expected)


class TestLeafNode(unittest.TestCase):
    def test_no_value_raises_error(self):
        with self.assertRaises(ValueError):
            node = LeafNode(HTMLType.PARAGRAPH, None)
            node.to_html()

    def test_text_only_node(self):
        node = LeafNode(None, "This is a value")
        self.assertEqual(node.to_html(), "This is a value")

    def test_paragraph_node(self):
        node = LeafNode(HTMLType.PARAGRAPH, "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_node_with_props(self):
        node = LeafNode(HTMLType.ANCHOR, "Click me!", {"href": "https://deloz.dev"})
        self.assertEqual(node.to_html(), '<a href="https://deloz.dev">Click me!</a>')
