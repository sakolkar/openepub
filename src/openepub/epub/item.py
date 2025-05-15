import bs4
import xml.parsers.expat as xml_expat
import xmltodict
import zipfile

import openepub as oe
from openepub.common import collect_text


class EpubItem:
    def __init__(self, package: "oe.EpubPackage", path: zipfile.Path, id: str):
        self.package = package
        self.path = path
        self.id = id


class EpubXHTMLItem(EpubItem):
    def __init__(self, package: "oe.EpubPackage", path: zipfile.Path, id: str):
        super().__init__(package, path, id)
        self.content_bytes = self.path.read_bytes()
        try:
            self.content_bytes.decode("utf-8", "strict")
        except UnicodeDecodeError:
            try:
                xmltodict.parse(self.content_bytes.decode("utf-8", "ignore"))
            except xml_expat.ExpatError:
                raise oe.DRMProtected("This content is protected by DRM.") from None
        self.soup = bs4.BeautifulSoup(
            self.content_bytes,
            "html.parser",
            from_encoding="utf-8",
        )

    def get_text(self):
        if self.soup.find("head") and self.soup.find("body"):
            text_soup = self.soup.find("body")
        else:
            text_soup = self.soup
        return collect_text(text_soup)
