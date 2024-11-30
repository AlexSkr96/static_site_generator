from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props={}):
        super().__init__(tag, value, [], props)


    def to_html(self):
        res = f"{self.get_tag_open()}{self.get_value()}{self.get_tag_close()}"
        return res
