from htmlnode import *
from textnode import *

def main():
    text = TextNode("This is a text node", TextType.BOLD.value, "https://deloz.dev")
    print(text)
    html_node = HTMLNode("h5", "This is a heading", None, {"href": "https://thisisalink.com", "target": "_blank"})
    print(html_node.props_to_html())

if __name__ == "__main__":
    main()
