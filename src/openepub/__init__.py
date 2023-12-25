__version__ = "0.0.4"


from .epub.epub import Epub
from .epub.item import EpubItem, EpubXHTMLItem
from .epub.package import EpubPackage
from .exceptions import EpubError, InvalidFileError, MalformedPackage


__all__ = [
    # Library Version
    __version__,
    # Core Classes
    Epub,
    EpubItem,
    EpubXHTMLItem,
    EpubPackage,
    # Exceptions
    EpubError,
    InvalidFileError,
    MalformedPackage,
]
