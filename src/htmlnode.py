class HTMLNode():
    def __init__(self, tag=None,
                 value=None,
                 children=None,
                 props=None):
        
        self.tag = tag
        self.value = value
        if not isinstance(children, list):
            if not children == None:
                raise TypeError(f"children must be list of HTMLNode, got {type(children)}")
        self.children = children
        self.props = props

    def to_html(self):
        #child classes will override
        raise NotImplementedError()

    def props_to_html(self):
        if self.props:
            return " " + " ".join(map(lambda prop: f'{prop}="{self.props[prop]}"', self.props))
        return None

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        if value is None:
            raise ValueError("leaf nodes are required to have a value")

    def to_html(self):
        if not self.value:
            raise ValueError("all leaf nodes must have a value")

        if not self.tag:
            return f"{self.value}"

        props = self.props_to_html()

        if self.tag is not None:
            return f"<{self.tag}{props if props else ""}>{self.value}</{self.tag}>"
        return f"{self.value}"

class ParentNode(HTMLNode):
    def __init__(self, tag,
                 children,
                 props: dict | None = None):
            self.tag = tag
            self.value = None
            self.children = children
            self.props = props

    def to_html(self):
        if not self.children:
            raise ValueError("parent nodes are required to have a child element")
        if not self.tag:
            raise ValueError("parent nodes are required to have a tag")
        props = self.props_to_html()
        result = ""
        for child in self.children:
            result += child.to_html()
        return f"<{self.tag}{props if props else ""}>{result}</{self.tag}>"
