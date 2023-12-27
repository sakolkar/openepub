import bs4
import typing
import xml.parsers.expat as xml_expat
import xmltodict
import zipfile

import openepub as oe


class EpubItem:
    def __init__(self, package: "oe.EpubPackage", path: zipfile.Path, id: str):
        self.package = package
        self.path = path
        self.id = id


class EpubXHTMLItem(EpubItem):
    def __init__(self, package: "oe.EpubPackage", path: zipfile.Path, id: str):
        super().__init__(package, path, id)
        try:
            self.content = self.path.read_text()
        except UnicodeDecodeError:
            raise oe.DRMProtected("This content is protected by DRM.") from None
        self.soup = bs4.BeautifulSoup(self.content, "html.parser")

    def get_text(self):
        for br in self.soup.find_all("br"):
            br.replace_with("\n")
        for tag in self.soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"]):
            if tag.previous_sibling != "\n":
                tag.insert_before("\n")
        if self.soup.find("head") and self.soup.find("body"):
            return self.soup.find("body").get_text()
        return self.soup.get_text()
