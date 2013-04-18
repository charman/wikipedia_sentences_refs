# -*- encoding: utf-8 -*-
import re
import unittest
from ddt import ddt, data
import mwparserfromhell
import get_data


text_Aquamole_Pot = u"""Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002.<ref>{{cite journal
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

text_Aquamole_Pot_replaced_ref = u"""Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002. coeref0 
blah"""

text_Aquamole_Pot_2_refs = u"""Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002.<ref>{{cite journal
 | author = Rupe Skorupka
 | year = 2002
 | month = October
 | title = A Pot Into Aquamole
 | journal = [[Descent (magazine)]]
 | issn = 0046-0036
 | issue = 168
 | pages = page 20–22
 | url = http://www.wildplaces.co.uk/descent/descent168.html
 }}</ref><ref>{{cite journal
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

text_Aquamole_Pot_2_replaced_refs = u"""Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002. coeref0  coeref1 
blah"""

text_Aquamole_Pot_no_url = u"""Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002.<ref>{{cite journal
 | author = Rupe Skorupka
 | year = 2002
 | month = October
 | title = A Pot Into Aquamole
 | journal = [[Descent (magazine)]]
 | issn = 0046-0036
 | issue = 168
 | pages = page 20–22
 }}</ref>
blah"""

text_Aquamole_Pot_no_url_without_ref = u"""Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002.
blah"""


class TestAquamolePot(unittest.TestCase):

    def setUp(self):
        self.title = 'https://en.wikipedia.org/wiki/Aquamole_Pot'

    def test_sentences(self):
        wikitext = get_data.scrape_wikitext('Aquamole Pot')
        expect = [
            'Aquamole Pot is a cave in West Kingsdale, North Yorkshire, England.',
            'It was originally explored from below by cave divers who had negotiated  of sump passage from Rowten Pot in 1974, to discover a high aven above the river passage.',
            'History',
            'The  aven was scaled in 1980 using poles, ladders and hand bolting kits, and a radio location transmitter placed at the highest point.',
            'Having discovered it was  from, and  below Jingling Pot, the aven was renamed Aquamole Aven instead of Jingling Avens.',
            'Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to  below the moor.',
            'It was finally connected to the surface in June 2002.'
            ]
        actual = get_data.split_sentences(wikitext)
        self.assertEqual(expect, actual)


wikicode = mwparserfromhell.parse(get_data.scrape_wikitext('Aquamole Pot'))

print wikicode
print
print wikicode.filter_templates(recursive=True, matches=r'cite')
print
print wikicode.strip_code()
print
print wikicode.filter_tags()
url_templates = wikicode.filter_templates(recursive=True, matches=r'cite.*')
print url_templates
for ut in url_templates:
    #print ut.get('url')
    if ut.has_param('url'):
        print ut.get('url').split('=')[-1].strip()
