from tempfile import TemporaryFile
from unittest import TestCase

from openepub import Epub, InvalidFileError, DRMProtected


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

    def test_open_epub_with_multiline_content(self):
        stream = TemporaryFile()
        with open("test/mock/hola_multiline.epub", "rb") as f:
            stream.write(f.read())
        epub_1 = Epub(stream=stream)
        text = epub_1.get_text()
        self.assertEqual(text, "Tengo un amigo.")

    def test_open_epub_with_drm(self):
        epub_1 = Epub("test/mock/hola_drm.epub")
        with self.assertRaises(DRMProtected):
            text = epub_1.get_text()

    def test_open_epub_with_nonutf(self):
        epub_1 = Epub("test/mock/hola_nonutf.epub")
        raw_content = list(list(epub_1.iterpackages())[0].iterspine())[0].content_bytes
        with self.assertRaises(UnicodeDecodeError):
            raw_content.decode("utf-8", "strict")
        text = epub_1.get_text()
        self.assertEqual(text, "Tengo un amigo. Tengo ¦ un amigo.")
