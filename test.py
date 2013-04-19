# -*- encoding: utf-8 -*-
import get_data
import re
import unittest

from string_scanner.scanner import Scanner
from ddt import ddt, data

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

result_Aquamole_Pot = [[u'Aquamole Pot is a cave in West Kingsdale, North Yorkshire, England.'], [u'It was originally explored from below by cave divers who had negotiated  of sump passage from Rowten Pot in 1974, to discover a high aven above the river passage.'], [u'History'], [u'The  aven was scaled in 1980 using poles, ladders and hand bolting kits, and a radio location transmitter placed at the highest point.'], [u'Having discovered it was  from, and  below Jingling Pot, the aven was renamed Aquamole Aven instead of Jingling Avens.', u'http://www.wildplaces.co.uk/descent/descent168.html'], [u'Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to  below the moor.'], [u'It was finally connected to the surface in June 2002.', u'http://www.wildplaces.co.uk/descent/descent168.html'], [u'References']]

#@ddt
class Test(unittest.TestCase):

    # @data(
    #     (text_Aquamole_Pot_no_url, text_Aquamole_Pot_no_url_without_ref),
    #     )

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
 | title = Kingsdale master cave, Yorkshire, Jingling Avens, Late reports Wórk
 | journal = [[Cave Diving Group|Cave diving group newsletter]]
 | issue = New series No.59
 | pages = page 12–13
 | url = http://www.wildplaces.co.uk/descent/descent168.html
 }}</ref>

Wórk"""

        scanner.string = expect
        token = u'Wórk'
        actual = get_data.get_next_wikitext_chunk(scanner, token)
        self.assertEqual(expect, actual)
