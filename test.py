# -*- encoding: utf-8 -*-
import get_data
import re
import unittest

from ddt import ddt, data


text_Aquamole_Pot = """Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002.<ref>{{cite journal
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

text_Aquamole_Pot_replaced_ref = """Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002. coeref0 
blah"""

text_Aquamole_Pot_2_refs = """Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002.<ref>{{cite journal
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

text_Aquamole_Pot_2_replaced_refs = """Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002. coeref0  coeref1 
blah"""

text_Aquamole_Pot_no_url = """Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002.<ref>{{cite journal
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

text_Aquamole_Pot_no_url_without_ref = """Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to {{convert|50|ft|m}} below the moor. It was finally connected to the surface in June 2002.
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


@ddt
class TestRefTag(unittest.TestCase):

    @data(
        (text_Aquamole_Pot_no_url, text_Aquamole_Pot_no_url_without_ref),
        )
    def test_remove_refs_with_no_url(self, value):
        input_data, expect = value
        self.assertEqual(expect, get_data.remove_refs_with_no_url(input_data))

    @data(
        (text_Aquamole_Pot, (text_Aquamole_Pot_replaced_ref, ['http://www.wildplaces.co.uk/descent/descent168.html'])),
        (text_Aquamole_Pot_2_refs, (text_Aquamole_Pot_2_replaced_refs, ['http://www.wildplaces.co.uk/descent/descent168.html', 'http://www.wildplaces.co.uk/descent/descent168.html'])),
        )
    def test_remove_refs_with_url(self, value):
        input_text, expect = value
        expect_changed_text, expect_ref_urls = expect
        actual_changed_text, actual_ref_urls = get_data.replace_refs_with_url(
            input_text
            ) 
        self.assertEqual(expect_changed_text, actual_changed_text)
        self.assertEqual(expect_ref_urls, actual_ref_urls)
