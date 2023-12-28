from bs4 import NavigableString
import re


def aslist(arg):
    if isinstance(arg, list):
        return arg
    if isinstance(arg, dict):
        return [arg]
    return list(arg)


def is_block_tag(tag_name):
    return tag_name in [
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "p",
        "li",
        "tr",
        "br",
        "div",
    ]


def collect_text(soup):
    text = ""
    if isinstance(soup, NavigableString):
        text = soup.text
        text = re.sub(r"\s+", r" ", text)
    elif hasattr(soup, "children"):
        for child in soup.children:
            child_text = collect_text(child)
            if is_block_tag(child.name):
                text += child_text + "\n\n"
            else:
                text += child_text
        text = "\n".join(line.strip() for line in text.splitlines())
    return text
