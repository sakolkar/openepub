from tempfile import TemporaryFile
from unittest import TestCase

from openepub import Epub, InvalidFileError


class EpubTestCase(TestCase):
    def test_open_get_epub_obj_valid_path(self):
        epub_1 = Epub("test/mock/tödliche_lektion.epub")
        self.assertIsInstance(epub_1, Epub)
        epub_2 = Epub("test/mock/tödliche_lektion.abcd")
        self.assertIsInstance(epub_2, Epub)

    def test_open_get_epub_obj_invalid_path(self):
        with self.assertRaises(InvalidFileError):
            Epub("test/mock/some_invalid_path.epub")
        with self.assertRaises(InvalidFileError):
            Epub(b"3.14159")

    def test_open_get_epub_obj_silly_path(self):
        with self.assertRaises(TypeError):
            Epub(3.14159)

    def test_open_get_epub_obj_invalid_file(self):
        with self.assertRaises(InvalidFileError):
            Epub("test/mock/not_an_epub.epub")

    def test_epub_get_text(self):
        epub_1 = Epub("test/mock/tödliche_lektion.epub")
        text = epub_1.get_text()
        stripped = text.strip()
        self.assertEqual("Naomi Novik", stripped[:11])
        self.assertEqual("DATENSCHUTZHINWEIS", stripped[-18:])

    def test_epub_get_text_2(self):
        epub_1 = Epub("test/mock/philosophers_stone.epub")
        text = epub_1.get_text()
        stripped = text.strip()
        self.assertTrue(stripped.startswith("Harry Potter and the Philosopher's Stone"))
        self.assertTrue(stripped.endswith("fun with Dudley this summer …’"))

    def test_open_epub_from_stream(self):
        stream = TemporaryFile()
        with open("test/mock/tödliche_lektion.epub", "rb") as f:
            stream.write(f.read())
        epub_1 = Epub(stream=stream)
        self.assertIsInstance(epub_1, Epub)
