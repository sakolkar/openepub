import typing
import xml.parsers.expat as xml_expat
import xmltodict
import zipfile

import openepub as oe
from openepub.common import aslist


class EpubPackage:
    def __init__(self, epub: "oe.Epub", path: zipfile.Path):
        self.epub = epub
        self.path = path
        self._package = self._read_package()
        if not self._package:
            raise oe.MalformedPackage(f"EPUB package file at {path.at} is malformed.")
        self.items = self._read_manifest()

    def _read_package(self) -> dict:
        try:
            content_bytes = self.path.read_bytes()
            package = xmltodict.parse(content_bytes.decode("utf-8", "ignore"))
            return package["package"]
        except (xml_expat.ExpatError, FileNotFoundError, KeyError, TypeError):
            pass
        return {}

    def _read_manifest(self) -> list:
        items = []
        try:
            for itemref in aslist(self._package["manifest"]["item"]):
                # TODO: In theory, the path can specify a scheme
                # see https://www.w3.org/TR/epub-33/#sec-item-elem
                # assuming it is a relative path for now.
                path = self.path.parent.joinpath(itemref["@href"])
                if not path.exists():
                    continue

                # TODO: Support other media types.
                if itemref["@media-type"] not in ("application/xhtml+xml", "text/html"):
                    continue

                items.append(
                    oe.EpubXHTMLItem(package=self, path=path, id=itemref["@id"])
                )
        except (KeyError, TypeError):
            return []
        return items

    def itermanifest(self):
        raise NotImplementedError("Iterating over the manifest is not yet supported.")

    def iterspine(self) -> typing.Iterator["oe.EpubItem"]:
        try:
            spine = aslist(self._package["spine"]["itemref"])
        except (KeyError, TypeError):
            spine = []
        for itemref in spine:
            if not isinstance(itemref, dict) or "@idref" not in itemref:
                continue
            item = self.get_item(itemref["@idref"])
            if item is None:
                continue
            yield item

    def get_item(self, id: str) -> typing.Union["oe.EpubItem", None]:
        return next(filter(lambda i: i.id == id, self.items), None)
