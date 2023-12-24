class EpubError(Exception):
    """
    Base exception class for all exceptions raised by the openepub library.
    """

    pass


class InvalidFileError(EpubError):
    """
    Indicates the file is invalid and does not conform to the EPUB specification.
    """

    pass


class MalformedPackage(EpubError):
    pass
