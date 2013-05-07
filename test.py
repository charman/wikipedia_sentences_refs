# -*- encoding: utf-8 -*-
import get_sents_refs
import scan_those_strings
import re
import unittest
import sys
from bs4 import BeautifulSoup
from string_scanner.scanner import Scanner
from ddt import ddt, data
import wiki2plain
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
<ref name="ref 1">{{cite journal
 | author = no url
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
 }}</ref><ref>{{cite something
 | author = Ian Watson
 | year = 1980
 | month = April
 | title = Kingsdale master cave, Yorkshire, Jingling Avens, Late reports Work
 | journal = [[Cave Diving Group|Cave diving group newsletter]]
 | issue = New series No.59
 | pages = page 12–13
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

wikitext_Aquamole_Pot_complicated_refs_replaced = u"""{{Infobox cave
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

'''Aquamole Pot''' is a cave in West [[Kingsdale]], [[North Yorkshire]], England. It was originally explored from below by cave divers who had negotiated {{convert|550|ft|m}} of [[Sump (cave)|sump]] passage from [[Rowten Pot]] in 1974, to discover a high [[Pitch (ascent/descent)|aven]] above the river passage. coeref0 
 coeref1 


==History==

The {{convert|130|ft|m}} aven was scaled in 1980 using poles, ladders and hand bolting kits, and a radio location transmitter placed at the highest point. Having discovered it was {{convert|180|ft|m}} from, and {{convert|180|ft|m}} below [[Jingling Pot]], the aven was renamed Aquamole Aven instead of Jingling Avens. coeref0  coeref2  

Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002. coeref0 

==References==
"""

result_Aquamole_Pot = [[], [], [], [], [u'http://www.wildplaces.co.uk/descent/descent168.html'], [], [u'http://www.wildplaces.co.uk/descent/descent168.html'], []]

#@ddt
class Test(unittest.TestCase):

    # @data(
    #     (text_Aquamole_Pot_no_url, text_Aquamole_Pot_no_url_without_ref),
    #     )

    def test_get_next_chunk(self):
        scanner = Scanner()
        expect = u""" Avens.<ref>{{cite journal
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


class TestComplicatedRefs(unittest.TestCase):

    maxDiff = None

    def test_collect_refs(self):
        expect = (
            {u'coeref0': [u'http://www.wildplaces.co.uk/descent/descent168.html',
                          u'http://www.wildplaces.co.uk/descent/descent170.html'],
             u'coeref1': [],
             u'coeref2': [u'http://www.wildplaces.co.uk/descent/descent168.html',
                          u'http://www.wildplaces.co.uk/descent/descent169.html'],
            },
            wikitext_Aquamole_Pot_complicated_refs_replaced
        )
        actual = scan_those_strings.collect_refs(wikitext_Aquamole_Pot_complicated_refs)
        sorted_mapping = {k: sorted(v) for k, v in actual[0].items()}
        actual = sorted_mapping, actual[1]
        self.assertEqual(expect[1], actual[1])
        self.assertEqual(expect[0], actual[0])

    def test_urls(self):
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
        actual = [sorted(list) for list in scan_those_strings.urls_for_lines(
            sentences_Aquamole_Pot,
            {u'coeref0': [u'http://www.wildplaces.co.uk/descent/descent168.html',
                          u'http://www.wildplaces.co.uk/descent/descent170.html'],
             u'coeref1': [],
             u'coeref2': [u'http://www.wildplaces.co.uk/descent/descent168.html',
                          u'http://www.wildplaces.co.uk/descent/descent169.html'],
            },
            unicode(wiki2plain.Wiki2Plain(wikitext_Aquamole_Pot_complicated_refs_replaced).text)
        )]
        self.assertEqual(expect, actual)


class TestFixupWikitext(unittest.TestCase):

    def test(self):
        bad_wikitext = u"""America."<ref name=páth/>

The dossier"""

        expect = u"""America."<ref name="páth" />

The dossier"""

        actual = get_sents_refs.fixup_named_refs(bad_wikitext)
        self.assertEqual(expect, actual)


class TestUrlExtraction(unittest.TestCase):

    def test_cited_urls_containing_equal_sign(self):
        wikitext = u'chanting the [[Litany of the Saints]].<ref name="YouTube procession">{{cite AV media | title = Procession and entrance in Conclave | trans_title = | medium = Television production | language = Italian | url = https://www.youtube.com/watch?v=cTtzyr5sBkc | accessdate = 9 April 2013 | date = 12 March 2013 | publisher = Centro Televisivo Vaticano | location = Rome | quote =}}</ref> After taking their places,'
        expect = [u'https://www.youtube.com/watch?v=cTtzyr5sBkc']
        actual = get_sents_refs.extract_ref_urls_from_wikitext(wikitext)
        self.assertEqual(expect, actual)

    def test_uncited_and_cited_urls_in_a_ref(self):
        wikitext = u"""unclear,<ref>Willey, David (28 February 2013). [http://www.bbc.co.uk/news/world-europe-21624154 "The day Benedict XVI's papacy ended"], [[BBC News]]. 1 March 2013.</ref> and that many different priorities were at play, making this election difficult to predict.<ref>{{cite web|url=http://www.bbc.co.uk/news/world-europe-21731439 |title=The Vatican: Suspense and intrigue |publisher=BBC |date=1 January 1970 |accessdate=12 March 2013}}</ref> Cardinal [[Cormac Murphy-O'Connor]] remarked laughingly to a BBC presenter that his colleagues have been telling him "Siamo confusi&nbsp;– 'we're confused,'" as there were neither clear blocs nor a front-runner.<ref>{{cite web|last=Ivereigh |first=Austen |url=http://www.osvdailytake.com/2013/03/ivereigh-in-rome-does-cardinal.html |title=OSV Daily Take Blog: Ivereigh in Rome: Does cardinal confusion spell a long conclave? |publisher=Osvdailytake.com |accessdate=12 March 2013}}</ref> blah"""
        expect = [u'http://www.bbc.co.uk/news/world-europe-21731439', u'http://www.osvdailytake.com/2013/03/ivereigh-in-rome-does-cardinal.html']
        actual = sorted(get_sents_refs.extract_ref_urls_from_wikitext(wikitext))
        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()


# TODO
# : multiple {{cite }} templates in a single ref
# : add {{cite}} in another named ref.
