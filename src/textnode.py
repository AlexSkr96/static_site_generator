from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.__text = text
        self.__text_type = text_type
        self.__url = url


    def __eq__(self, textnode):
        if (self.__text == textnode.get_text() and
            self.__text_type == textnode.get_text_type() and
            self.__url == textnode.get_url()):
            return True
        else:
            return False


    def __repr__(self):
        return f"TextNode({self.__text}, {self.__text_type.value}, {self.__url})"


    def get_text(self):
        return self.__text


    def get_text_type(self):
        return self.__text_type


    def get_url(self):
        return self.__url
