import re


def markdown_to_blocks(markdown):
    blocks = []
    markdown_list = markdown.strip().split("\n") + [""]
    block = ""
    for row in markdown_list:
        row = row.strip()
        if len(row) > 0:
            block += f"{row}\n"
        elif len(block) > 0:
            blocks.append(block)
            block = ""

    return blocks


def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return "heading"
    elif re.match(r"^```(.|\n)*```$", block) and "```" not in block[3:-3]:
        return "code"
    elif re.match(r"^>", block):
        for line in block.split("\n")[1:]:
            if not re.match(r"^>", line):
                return "normal"

        return "quote"
    elif re.match(r"^[\*-] ", block):
        for line in block.split("\n")[1:]:
            if not re.match(r"^[\*-] ", line):
                return "normal"

        return "unorderd"
    elif re.match(r"^[0-9]\. ", block):
        for line in block.split("\n")[1:]:
            if not re.match(r"^[0-9]\. ", line):
                return "normal"

        return "orderd"
    else:
        return "normal"
