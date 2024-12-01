from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = {}):
        super().__init__(tag=tag, children=children, props=props)


    def to_html(self, pretty=False):
        if pretty == True:
            print("Pretty to_html not yet implemented!")

        if not self.get_tag_pure() or self.get_tag_pure() == "":
            raise ValueError("No tag!")
        elif not self.get_children():
            raise ValueError("No children!")
        else:
            res = self.get_tag_open()
            for child in self.get_children():
                res += child.to_html()

            res += self.get_tag_close()

            return res
