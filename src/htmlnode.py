class HTMLNode():
    def __init__(self, tag=None, value=None, children=[], props={}):
        self.__tag = tag
        self.__value = value
        self.__children = children
        self.__props = props


    def __repr__(self):
        res = f"HTMLNode(<{self.__tag}>, {self.__value}, {len(self.__children)} children,\n {self.__props})"
        return res


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
        return f"<{self.__tag}{self.props_to_html()}>"


    def get_tag_close(self):
        return f"</{self.__tag}>"


    def get_value(self):
        return self.__value


    def get_children(self):
        return self.__children
