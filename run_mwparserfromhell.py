# -*- encoding: utf-8 -*-
import re
import unittest
from ddt import ddt, data
import mwparserfromhell
import get_data

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
