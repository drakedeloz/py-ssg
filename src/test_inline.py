import unittest

from inline import *
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(nodes) == 3

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("This **bold** and **more bold**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(nodes) == 4

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

class TestMarkdownExtraction(unittest.TestCase):
    def test_show_matches_images(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        assert matches == [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]

    def test_show_matches_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        assert matches == [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

    def test_show_matches_images_empty(self):
        matches = extract_markdown_images("""
                                            Here's a [link](http://example.com) and an ![image](img.jpg)
                                            and another [link!](not-an-image) and ![](empty-alt)
                                            """)
        assert matches == [('image', 'img.jpg'), ('', 'empty-alt')]

    def test_show_matches_links_empty(self):
        matches = extract_markdown_links("""
                                            Here's a [link](http://example.com) and an ![image](img.jpg)
                                            and another [link!](not-an-image) and ![](empty-alt)
                                            """)
        assert matches == [('link', 'http://example.com'), ('link!', 'not-an-image')]

class TestSplitNodesImages(unittest.TestCase):
    def test_split_nodes_image_no_image(self):
        node = TextNode("Just plain text", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert nodes == [TextNode("Just plain text", TextType.TEXT)]

    def test_split_nodes_image_single(self):
        node = TextNode("Hello ![alt](http://image.png) world", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert nodes == [
            TextNode("Hello ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "http://image.png"),
            TextNode(" world", TextType.TEXT)
        ]

    def test_split_nodes_image_multiple(self):
        node = TextNode(
            "Start ![one](http://one.png) middle ![two](http://two.png) end",
            TextType.TEXT
        )
        nodes = split_nodes_image([node])
        assert nodes == [
            TextNode("Start ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "http://one.png"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "http://two.png"),
            TextNode(" end", TextType.TEXT)
        ]
        

    def test_split_nodes_image_at_start(self):
        node = TextNode("![start](http://start.png) then text", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert nodes == [
            TextNode("start", TextType.IMAGE, "http://start.png"),
            TextNode(" then text", TextType.TEXT)
        ]

    def test_split_nodes_image_at_end(self):
        node = TextNode("Some text ![end](http://end.png)", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert nodes == [
            TextNode("Some text ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "http://end.png")
        ]

class TestSplitNodesLinks(unittest.TestCase):
    def test_split_nodes_links_no_link(self):
        node = TextNode("Just plain text", TextType.TEXT)
        nodes = split_nodes_links([node])
        assert nodes == [TextNode("Just plain text", TextType.TEXT)]

    def test_split_nodes_links_single(self):
        node = TextNode("Hello [alt](http://image.png) world", TextType.TEXT)
        nodes = split_nodes_links([node])
        assert nodes == [
            TextNode("Hello ", TextType.TEXT),
            TextNode("alt", TextType.LINK, "http://image.png"),
            TextNode(" world", TextType.TEXT)
        ]

    def test_split_nodes_links_multiple(self):
        node = TextNode(
            "Start [one](http://one.png) middle [two](http://two.png) end",
            TextType.TEXT
        )
        nodes = split_nodes_links([node])
        assert nodes == [
            TextNode("Start ", TextType.TEXT),
            TextNode("one", TextType.LINK, "http://one.png"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("two", TextType.LINK, "http://two.png"),
            TextNode(" end", TextType.TEXT)
        ]
        

    def test_split_nodes_link_at_start(self):
        node = TextNode("[start](http://start.png) then text", TextType.TEXT)
        nodes = split_nodes_links([node])
        assert nodes == [
            TextNode("start", TextType.LINK, "http://start.png"),
            TextNode(" then text", TextType.TEXT)
        ]

    def test_split_nodes_link_at_end(self):
        node = TextNode("Some text [end](http://end.png)", TextType.TEXT)
        nodes = split_nodes_links([node])
        assert nodes == [
            TextNode("Some text ", TextType.TEXT),
            TextNode("end", TextType.LINK, "http://end.png")
        ]

class TestTextToNodes(unittest.TestCase):
    def test_text_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        print(nodes)
        assert nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
