import unittest

from htmlnode import HTMLNode, HTMLType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(HTMLType.PARAGRAPH, "This is a paragraph of text", None, {"styles": "font-family:Garamond;color:red;"})
        print(node.props_to_html())

    def test_props_to_html2(self):
        node = HTMLNode(HTMLType.heading(1), "This is a heading")
        print(node.props_to_html())

    def test_repr(self):
        node = HTMLNode(HTMLType.heading(2), "This is a heading", None, {"styles": "font-family:Times;color:blue"})
        print(node)

