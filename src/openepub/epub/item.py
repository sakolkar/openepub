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
        self.content = self.path.read_text()
        self.soup = bs4.BeautifulSoup(self.content, "html.parser")

    def get_text(self):
        for br in self.soup.find_all("br"):
            br.replace_with("\n")
        if self.soup.find("head") and self.soup.find("body"):
            return self.soup.find("body").get_text()
        return self.soup.get_text()
