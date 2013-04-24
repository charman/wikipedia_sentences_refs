# -*- encoding: utf-8 -*-
import get_data
import re
import unittest
import sys
from bs4 import BeautifulSoup
from string_scanner.scanner import Scanner
from ddt import ddt, data
import pprint
pp = pprint.PrettyPrinter()

sentences_Aquamole_Pot = [
    u'Aquamole Pot is a cave in West Kingsdale, North Yorkshire, England.',
    u'It was originally explored from below by cave divers who had negotiated  of sump passage from Rowten Pot in 1974, to discover a high aven above the river passage.',
    u'History',
    u'The  aven was scaled in 1980 using poles, ladders and hand bolting kits, and a radio location transmitter placed at the highest point.',
    u'Having discovered it was  from, and  below Jingling Pot, the aven was renamed Aquamole Aven instead of Jingling Avens.',
    u'Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to  below the moor.',
    u'It was finally connected to the surface in June 2002.',
    u'References',
]

wikitext_Aquamole_Pot = u"""{{Infobox cave
| name = Aquamole Pot
| photo =
| photo_caption =
| location = [[West Kingsdale]], [[North Yorkshire]], [[UK]]
| depth = {{convert|113|m}}
| length = {{convert|142|m}}
| coords =
| discovery = 1974
| geology = [[Limestone]]
| bcra_grade = 4b
| grid_ref_UK = SD 69926 78338
| map = United Kingdom Yorkshire Dales
| map_width =
| lat_d = 54.199909
| long_d = -2.462490
| location_public = yes
| entrance_count = 2
| access = Free
| survey = [http://cavemaps.org/cavePages/West%20Kingsdale__Aquamole%20Pot.htm cavemaps.org]
}}

'''Aquamole Pot''' is a cave in West [[Kingsdale]], [[North Yorkshire]], England. It was originally explored from below by cave divers who had negotiated {{convert|550|ft|m}} of [[Sump (cave)|sump]] passage from [[Rowten Pot]] in 1974, to discover a high [[Pitch (ascent/descent)|aven]] above the river passage.<ref>{{cite journal
 | author = Geoff Yeaden
 | year = 1974
 | month = July
 | title = Kingsdale master cave, Yorkshire
 | journal = [[Cave Diving Group|Cave diving group newsletter]]
 | issue = New series No.32
 | pages = page 16–18
 }}</ref>

==History==

The {{convert|130|ft|m}} aven was scaled in 1980 using poles, ladders and hand bolting kits, and a radio location transmitter placed at the highest point. Having discovered it was {{convert|180|ft|m}} from, and {{convert|180|ft|m}} below [[Jingling Pot]], the aven was renamed Aquamole Aven instead of Jingling Avens.<ref>{{cite journal
 | author = Ian Watson
 | year = 1980
 | month = April
 | title = Kingsdale master cave, Yorkshire, Jingling Avens, Late reports Work
 | journal = [[Cave Diving Group|Cave diving group newsletter]]
 | issue = New series No.59
 | pages = page 12–13
 | url = http://www.wildplaces.co.uk/descent/descent168.html
 }}</ref>

Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002.<ref>{{cite journal
 | author = Rupe Skorupka
 | year = 2002
 | month = October
 | title = A Pot Into Aquamole
 | journal = [[Descent (magazine)]]
 | issn = 0046-0036
 | issue = 168
 | pages = page 20–22
 | url = http://www.wildplaces.co.uk/descent/descent168.html
 }}</ref>

==References==
"""

wikitext_Aquamole_Pot_complicated_refs = u"""{{Infobox cave
| name = Aquamole Pot
| photo =
| photo_caption =
| location = [[West Kingsdale]], [[North Yorkshire]], [[UK]]
| depth = {{convert|113|m}}
| length = {{convert|142|m}}
| coords =
| discovery = 1974
| geology = [[Limestone]]
| bcra_grade = 4b
| grid_ref_UK = SD 69926 78338
| map = United Kingdom Yorkshire Dales
| map_width =
| lat_d = 54.199909
| long_d = -2.462490
| location_public = yes
| entrance_count = 2
| access = Free
| survey = [http://cavemaps.org/cavePages/West%20Kingsdale__Aquamole%20Pot.htm cavemaps.org]
}}

'''Aquamole Pot''' is a cave in West [[Kingsdale]], [[North Yorkshire]], England. It was originally explored from below by cave divers who had negotiated {{convert|550|ft|m}} of [[Sump (cave)|sump]] passage from [[Rowten Pot]] in 1974, to discover a high [[Pitch (ascent/descent)|aven]] above the river passage.<ref name="ref 0">{{cite journal
 | author = Geoff Yeaden
 | year = 1974
 | month = July
 | title = Kingsdale master cave, Yorkshire
 | journal = [[Cave Diving Group|Cave diving group newsletter]]
 | issue = New series No.32
 | pages = page 16–18
 }}</ref>

==History==

The {{convert|130|ft|m}} aven was scaled in 1980 using poles, ladders and hand bolting kits, and a radio location transmitter placed at the highest point. Having discovered it was {{convert|180|ft|m}} from, and {{convert|180|ft|m}} below [[Jingling Pot]], the aven was renamed Aquamole Aven instead of Jingling Avens.<ref name = "ref 0" /><ref>{{cite journal
 | author = Ian Watson
 | year = 1980
 | month = April
 | title = Kingsdale master cave, Yorkshire, Jingling Avens, Late reports Work
 | journal = [[Cave Diving Group|Cave diving group newsletter]]
 | issue = New series No.59
 | pages = page 12–13
 | url = http://www.wildplaces.co.uk/descent/descent168.html
 }}{{cite something
 | author = Ian Watson
 | year = 1980
 | month = April
 | title = Kingsdale master cave, Yorkshire, Jingling Avens, Late reports Work
 | journal = [[Cave Diving Group|Cave diving group newsletter]]
 | issue = New series No.59
 | pages = page 12–13
 | url = http://www.wildplaces.co.uk/descent/descent169.html
 }}</ref>

Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002.<ref name ='ref 0'>{{cite journal
 | author = Rupe Skorupka
 | year = 2002
 | month = October
 | title = A Pot Into Aquamole
 | journal = [[Descent (magazine)]]
 | issn = 0046-0036
 | issue = 168
 | pages = page 20–22
 | url = http://www.wildplaces.co.uk/descent/descent168.html
 }}{{cite something
 | author = Ian Watson
 | year = 1980
 | month = April
 | title = Kingsdale master cave, Yorkshire, Jingling Avens, Late reports Work
 | journal = [[Cave Diving Group|Cave diving group newsletter]]
 | issue = New series No.59
 | pages = page 12–13
 | url = http://www.wildplaces.co.uk/descent/descent170.html
 }}</ref>

==References==
"""

result_Aquamole_Pot = [[], [], [], [], [u'http://www.wildplaces.co.uk/descent/descent168.html'], [], [u'http://www.wildplaces.co.uk/descent/descent168.html'], []]

#@ddt
class Test(unittest.TestCase):

    # @data(
    #     (text_Aquamole_Pot_no_url, text_Aquamole_Pot_no_url_without_ref),
    #     )

    #@unittest.skip('')
    def test_remove_refs_with_no_url(self):
        self.assertEqual(
            result_Aquamole_Pot,
            get_data.collect_citations(
                sentences_Aquamole_Pot,
                wikitext_Aquamole_Pot
            )
        )

    def test_get_next_chunk(self):
        scanner = Scanner()
        expect = u"""Avens.<ref>{{cite journal
 | author = Ian Watson
 | year = 1980
 | month = April
 | title = Kingsdale master cave, Yorkshire, Jingling Avens, Late reports W\u006Frk
 | journal = [[Cave Diving Group|Cave diving group newsletter]]
 | issue = New series No.59
 | pages = page 12–13
 | url = http://www.wildplaces.co.uk/descent/descent168.html
 }}</ref>

W\u006Frk"""

        scanner.string = expect
        token = u'W\u006Frk'
        actual = get_data._get_next_wikitext_chunk(scanner, token)
        self.assertEqual(expect, actual)


class TestComplicatedRefs(unittest.TestCase):

    def test_refs(self):
        # Note: 'ref 0' consists of:
        #   ['http://www.wildplaces.co.uk/descent/descent168.html',
        #    'http://www.wildplaces.co.uk/descent/descent170.html'],
        expect = [
            [],
            [u'http://www.wildplaces.co.uk/descent/descent168.html',
             u'http://www.wildplaces.co.uk/descent/descent170.html'],
            [],
            [],
            [u'http://www.wildplaces.co.uk/descent/descent168.html',
             u'http://www.wildplaces.co.uk/descent/descent169.html',
             u'http://www.wildplaces.co.uk/descent/descent170.html'],
            [],
            [u'http://www.wildplaces.co.uk/descent/descent168.html',
             u'http://www.wildplaces.co.uk/descent/descent170.html'],
            [],
        ]
        actual = [sorted(list) for list in get_data.collect_citations(
            sentences_Aquamole_Pot,
            wikitext_Aquamole_Pot_complicated_refs,
        )]
        pp.pprint(expect)
        pp.pprint(actual)
        self.assertEqual(expect, actual)

    def test_get_ref_names_citations(self):
        expect = {
            'ref 0': [u'http://www.wildplaces.co.uk/descent/descent168.html',
                      u'http://www.wildplaces.co.uk/descent/descent170.html'],
        }
        actual = get_data.get_ref_names_citations(
            wikitext_Aquamole_Pot_complicated_refs
        )

        self.assertEqual(expect.keys(), actual.keys())

        for key in expect.keys():
            self.assertEqual(
                sorted(expect[key]),
                sorted(actual[key])
            )


class TestREs(unittest.TestCase):

    def test_open_tag(self):
        self.assertTrue(get_data.TAG_OPEN_RE.search(' <ref> '))
        self.assertTrue(get_data.TAG_OPEN_RE.search(' < ref > '))
        self.assertTrue(get_data.TAG_OPEN_RE.search(' <ref name="hello"> '))
        self.assertFalse(get_data.TAG_OPEN_RE.search(' </ref> '))
        self.assertFalse(get_data.TAG_OPEN_RE.search(' <ref /> '))
        self.assertFalse(get_data.TAG_OPEN_RE.search(' <ref name="hello"/> '))
        self.assertFalse(get_data.TAG_CLOSE_RE.search(' <ref name="hello" /> '))
        self.assertFalse(get_data.TAG_CLOSE_RE.search(' < ref name="hello" /> '))

    def test_close_tag(self):
        self.assertFalse(get_data.TAG_CLOSE_RE.search(' <ref> '))
        self.assertFalse(get_data.TAG_CLOSE_RE.search(' < ref > '))
        self.assertFalse(get_data.TAG_CLOSE_RE.search(' <ref name="hello"> '))
        self.assertTrue(get_data.TAG_CLOSE_RE.search(' </ref> '))
        self.assertFalse(get_data.TAG_CLOSE_RE.search(' <ref /> '))
        self.assertFalse(get_data.TAG_CLOSE_RE.search(' <ref name="hello"/> '))
        self.assertFalse(get_data.TAG_CLOSE_RE.search(' <ref name="hello" /> '))
        self.assertFalse(get_data.TAG_CLOSE_RE.search(' < ref name="hello" /> '))

    def test_openclose_tag(self):
        self.assertFalse(get_data.TAG_OPENCLOSE_RE.search(' <ref> '))
        self.assertFalse(get_data.TAG_OPENCLOSE_RE.search(' < ref > '))
        self.assertFalse(get_data.TAG_OPENCLOSE_RE.search(' <ref name="hello"> '))
        self.assertFalse(get_data.TAG_OPENCLOSE_RE.search(' </ref> '))
        self.assertTrue(get_data.TAG_OPENCLOSE_RE.search(' <ref /> '))
        self.assertTrue(get_data.TAG_OPENCLOSE_RE.search(' <ref name="hello"/> '))
        self.assertTrue(get_data.TAG_OPENCLOSE_RE.search(' <ref name="hello" /> '))
        self.assertTrue(get_data.TAG_OPENCLOSE_RE.search(' < ref name="hello" /> '))


# TODO
# : multiple {{cite }} templates in a single ref
# : add {{cite}} in another named ref.
