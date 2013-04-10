# -*- encoding: utf-8 -*-
import get_data
import unittest


class TestAquamolePot(unittest.TestCase):

    def setUp(self):
        self.title = 'https://en.wikipedia.org/wiki/Aquamole_Pot'

    def test_sentences(self):
        expect = [
            'Aquamole Pot is a cave in West Kingsdale, North Yorkshire, '
                'England.',
            'It was originally explored from below by cave divers who had '
                'negotiated 550 feet (170 m) of sump passage from Rowten Pot '
                'in 1974, to discover a high aven above the river passage.',
            'History',
            'The 130 feet (40 m) aven was scaled in 1980 using poles, '
                'ladders and hand bolting kits, and a radio location '
                'transmitter placed at the highest point.',
            'Having discovered it was 180 feet (55 m) from, and 180 feet (55 '
                'm) below Jingling Pot, the aven was renamed Aquamole Aven '
                'instead of Jingling Avens.',
            'Work restarted in 2000 when divers who were keen on a quick '
                'route to the sump beyond, rescaled the avens to a higher '
                'point, and radio located a position to 50 feet (15 m) below '
                'the moor.',
            'It was finally connected to the surface in June 2002.'
        ]
        actual = get_data.scrape_wikitext('Aquamole Pot')
        self.assertEqual(expect, actual)


text = """Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002.<ref>{{cite journal
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
 blah"""

#import xml.etree.ElementTree as ET
#tree = ET.fromstring(text)
#for r in tree.findall('ref'):
#    print(r.text)


from pprint import pprint
from bs4 import BeautifulSoup
soup = BeautifulSoup(text)

refs = soup.find_all('ref')
for r in refs:
    r.replace_with('ref0')
pprint(soup.text)
