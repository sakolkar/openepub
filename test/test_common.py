from unittest import TestCase

import bs4

from openepub import Epub
from openepub.common import collect_text


class CollectTextTestCase(TestCase):
    def test_multiple_spans_in_p(self):
        """
        Test to make sure that if there are span elements within block elements
        their spaces aren't trimmed from the ends.

        Targets a fix for github issue #2.
        """

        source = (
            """<p><span>Odpovědi na tyto a mnohé další otázky hledá v novém"""
            """ senzačním životopise nazvaném </span><span>Život a lži Albu"""
            """se Brumbála</span><span> Rita Holoubková. Exkluzivní rozhovo"""
            """r s ní přináší Betty Braithwaiteová na straně 13.</span></p>"""
        )

        expected = (
            """Odpovědi na tyto a mnohé další otázky hledá v novém senzační"""
            """m životopise nazvaném Život a lži Albuse Brumbála Rita Holou"""
            """bková. Exkluzivní rozhovor s ní přináší Betty Braithwaiteová"""
            """ na straně 13.\n"""
        )

        soup = bs4.BeautifulSoup(source.encode("utf-8"), "html.parser")
        collected = collect_text(soup)

        self.assertEqual(collected, expected)

    def test_romeo_and_juliet(self):
        """
        Test to make sure we are reading Romeo & Juliet correctly.
        """

        epub = Epub("test/mock/prj_gb_romeo_and_juliet.epub")
        with open("test/mock/prj_gb_romeo_and_juliet.txt", "r") as f:
            expected = f.read()
        collected = epub.get_text()

        self.assertEqual(collected, expected)
        
    def test_right_to_left(self):
        """
        Test to make sure a right-to-left language (Farsi) book is being read
        correctly.        
        """

        epub = Epub("test/mock/prj_gb_five_selected_short_stories_farsi.epub")
        with open("test/mock/prj_gb_five_selected_short_stories_farsi.txt", "r") as f:
            expected = f.read()
        collected = epub.get_text()

        self.assertEqual(collected, expected)
