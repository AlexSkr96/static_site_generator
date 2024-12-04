from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = {}):
        super().__init__(tag=tag, children=children, props=props)


    def to_html(self, pretty=False, tabs=0):
        if not self.get_tag_pure() or self.get_tag_pure() == "":
            raise ValueError("No tag!")
        elif not self.get_children():
            raise ValueError("No children!")
        else:
            res = ""
            res += self.get_tag_open()
            if pretty: res += "\n"
            for child in self.get_children():
                if pretty: res += "\t"*(tabs+1)
                res += child.to_html(pretty=pretty, tabs=tabs+1)
                if pretty: res += "\n"

            if pretty: res += "\t"*tabs
            res += self.get_tag_close()

            return res
