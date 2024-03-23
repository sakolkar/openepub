from unittest import TestCase

import bs4

from openepub.common import collect_text


class CollectTextTestCase(TestCase):
    def test_multiple_spans_in_p(self):

        source = (
            """<p class="Clanek1"><span lang="CS">Odpovědi na tyto a mnohé """
            """další otázky hledá v novém senzačním životopise nazvaném </s"""
            """pan><span lang="CS">Život a lži Albuse Brumbála</span><span """
            """lang="CS"> Rita Holoubková. Exkluzivní rozhovor s ní přináší"""
            """ Betty Braithwaiteová na straně 13.</span></p>"""
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