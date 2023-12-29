import os
import typing
import xml.parsers.expat as xml_expat
import xmltodict
import zipfile

import openepub as oe
from openepub.common import aslist


class Epub:
    def __init__(self, path=None, stream=None):
        if path is None and stream is None or path is not None and stream is not None:
            raise ValueError("One of path or stream must be specified.")

        if path is None:
            pass
        elif isinstance(path, (str, bytes, os.PathLike)):
            if not os.path.exists(path):
                raise oe.InvalidFileError("Specified path does not exist.")
            path_or_stream = path
        else:
            raise TypeError("path argument must be path-like.")

        if stream is None:
            pass
        elif hasattr(stream, "read"):
            path_or_stream = stream
        else:
            raise TypeError("stream argument must be file-like.")

        if not zipfile.is_zipfile(path_or_stream):
            raise oe.InvalidFileError("File specified is not an EPUB.")

        self.zip = zipfile.ZipFile(path_or_stream, mode="r")
        self.root = zipfile.Path(self.zip)

        self.package_paths = self._read_package_paths()
        if not self.package_paths:
            raise oe.InvalidFileError("File specified is not an EPUB.")

    def _read_package_paths(self) -> list:
        package_paths = []
        try:
            content_bytes = (self.root / "META-INF" / "container.xml").read_bytes()
            container = xmltodict.parse(content_bytes.decode("utf-8", "ignore"))
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
        return "\n".join(texts).strip()
