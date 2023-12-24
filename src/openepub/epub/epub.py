import os
import typing
import xml.parsers.expat as xml_expat
import xmltodict
import zipfile

import openepub as oe
from openepub.common import aslist


class Epub:
    def __init__(self, path=None):
        if not isinstance(path, (str, bytes, os.PathLike)):
            raise TypeError("path argument must be path-like.")
        if not os.path.exists(path):
            raise oe.InvalidFileError("Specified path does not exist.")
        if not zipfile.is_zipfile(path):
            raise oe.InvalidFileError("File at specified path is not an EPUB.")

        self.zip = zipfile.ZipFile(path, mode="r")
        self.root = zipfile.Path(self.zip)

        self.package_paths = self._read_package_paths()
        if not self.package_paths:
            raise oe.InvalidFileError("File at specified path is not an EPUB.")

    def _read_package_paths(self) -> list:
        package_paths = []
        try:
            container = xmltodict.parse(
                (self.root / "META-INF" / "container.xml").read_text()
            )
            for rootfile in aslist(container["container"]["rootfiles"]["rootfile"]):
                path = self.root.joinpath(rootfile["@full-path"])
                if not path.exists():
                    raise ValueError("EPUB rootfile has an invalid path.")
                package_paths.append(path)
        except (
            xml_expat.ExpatError,
            FileNotFoundError,
            KeyError,
            TypeError,
            ValueError,
        ):
            return []
        return package_paths

    def iterpackages(self) -> typing.Iterator["oe.EpubPackage"]:
        for path in self.package_paths:
            yield oe.EpubPackage(epub=self, path=path)

    def get_text(self):
        texts = []
        for package in self.iterpackages():
            for item in package.iterspine():
                texts.append(item.get_text())
        return "\n".join(texts)
