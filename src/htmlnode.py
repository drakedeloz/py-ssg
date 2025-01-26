from enum import Enum

class HTMLType(Enum):
    TEXT = "text"
    PARAGRAPH = "p"
    ANCHOR = "a"

    @classmethod
    def heading(cls, level: int) -> str:
        if not isinstance(level, int) or level < 1 or level > 6:
            raise ValueError("Heading level must be an integer between 1 and 6")
        return f"h{level}"

class HTMLNode():
    def __init__(self, tag: HTMLType | None = None,
                 value: str | None = None,
                 children=None,
                 props: dict | None = None):
        
        self.tag = tag
        self.value = value
        if not isinstance(children, list) or not all(isinstance(x, HTMLNode) for x in children):
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

