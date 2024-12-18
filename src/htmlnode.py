class HTMLNode():
    def __init__(self, tag=None, value=None, children=[], props={}):
        self.__tag = tag
        self.__value = value
        self.__children = children
        self.__props = props


    def __repr__(self):
        tag = f"<{self.__tag}>" if self.__tag else None
        res = f"HTMLNode({tag}, \"{self.__value}\", {len(self.__children)} children, {self.__props})"
        return res

    def __eq__(self, html_node):
        if (self.__tag == html_node.get_tag_pure() and
            self.__value == html_node.get_value() and
            self.__children == html_node.get_children() and
            self.__props == html_node.get_props()
        ):
            return True
        else:
            return False

    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        res = ""
        for key in self.__props:
            res += f' {key}={self.__props[key]}'

        return res


    def get_tag_pure(self):
        return self.__tag


    def get_tag_open(self):
        if self.__tag and len(self.__tag) > 0:
            return f"<{self.__tag}{self.props_to_html()}>"
        else:
            return ""


    def get_tag_close(self):
        if self.__tag and len(self.__tag) > 0:
            return f"</{self.__tag}>"
        else:
            return ""


    def get_value(self):
        return self.__value


    def get_children(self):
        return self.__children


    def get_props(self):
        return self.__props
