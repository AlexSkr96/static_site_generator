from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props={}):
        if value == None:
            return ValueError("")

        super().__init__(tag, value, [], props)


    def to_html(self, pretty=False, tabs=0):
        res = f"{self.get_tag_open()}{self.get_value()}{self.get_tag_close()}"
        return res
