import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "p", 
            "This is a paragraph of text", 
            None, 
            {"styles": "font-family:Garamond;color:red;"}
        )
        self.assertEqual(
            node.props_to_html(), 
            ' styles="font-family:Garamond;color:red;"'
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode("h1", "This is a heading")
        self.assertIsNone(node.props_to_html())

    def test_repr(self):
        node = HTMLNode(
            "h2", 
            "This is a heading", 
            None, 
            {"styles": "font-family:Times;color:blue"}
        )
        expected = 'HTMLNode(h2, This is a heading, None, {\'styles\': \'font-family:Times;color:blue\'})'
        self.assertEqual(str(node), expected)


class TestLeafNode(unittest.TestCase):
    def test_no_value_raises_error(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

    def test_text_only_node(self):
        node = LeafNode(None, "This is a value")
        self.assertEqual(node.to_html(), "This is a value")

    def test_paragraph_node(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_node_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://deloz.dev"})
        self.assertEqual(node.to_html(), '<a href="https://deloz.dev">Click me!</a>')

class TestParentNode(unittest.TestCase):
    def test_parent_node_basic(self):
        node = ParentNode("div", [LeafNode(None, "Hello")])
        assert node.to_html() == "<div>Hello</div>"

    def test_parent_node_missing_tag(self):
        try:
            node = ParentNode(None, [LeafNode(None, "Hello")])
            node.to_html()
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_parent_node_missing_children(self):
        try:
            node = ParentNode("div", None)
            node.to_html()
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_parent_node_complex_nesting(self):
        inner_parent = ParentNode("div", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text")
        ])
        
        outer_parent = ParentNode("section", [
            LeafNode("h1", "Title"),
            inner_parent,
            LeafNode("p", "Paragraph")
        ])
        
        expected = "<section><h1>Title</h1><div><b>Bold text</b>Normal text</div><p>Paragraph</p></section>"
        assert outer_parent.to_html() == expected

    def test_parent_node_with_props(self):
        node = ParentNode("div", 
            [
                LeafNode("p", "Text", {"class": "highlight"}),
                LeafNode(None, "Plain text"),
                ParentNode("span", [
                    LeafNode("i", "Italic")
                ], {"id": "special"})
            ],
            {"class": "container", "data-test": "true"}
        )
        expected = '<div class="container" data-test="true"><p class="highlight">Text</p>Plain text<span id="special"><i>Italic</i></span></div>'
        assert node.to_html() == expected
