# -*- encoding: utf-8 -*-
import get_sents_refs
import re
import unittest
import sys
from bs4 import BeautifulSoup
from scanner import Scanner
#from ddt import ddt, data
import wiki2plain

def parallel_print(list1, list2):
    list1.extend(["", ""])
    list2.extend(["", ""])
    return '\n'.join([
        "{:<40}{:<40}".format(l, r)
        for l, r in zip(list2, list1)
    ])

cloud_links = """
<?xml version="1.0"?>
<api>
  <query>
    <pages>
      <page pageid="47515" ns="0" title="Cloud">
        <langlinks>
          <ll lang="af" xml:space="preserve">Wolk</ll>
          <ll lang="an" xml:space="preserve">Boira</ll>
          <ll lang="ang" xml:space="preserve">Wolcen</ll>
          <ll lang="ar" xml:space="preserve">سحاب</ll>
          <ll lang="arc" xml:space="preserve">ܥܢܢܐ</ll>
          <ll lang="ast" xml:space="preserve">Nube</ll>
          <ll lang="ay" xml:space="preserve">Qinaya</ll>
          <ll lang="az" xml:space="preserve">Bulud</ll>
          <ll lang="ba" xml:space="preserve">Болот</ll>
          <ll lang="bat-smg" xml:space="preserve">Debesis</ll>
          <ll lang="be" xml:space="preserve">Воблакі</ll>
          <ll lang="be-x-old" xml:space="preserve">Хмара</ll>
          <ll lang="bg" xml:space="preserve">Облак</ll>
          <ll lang="bjn" xml:space="preserve">Rakun (météorologi)</ll>
          <ll lang="bn" xml:space="preserve">মেঘ</ll>
          <ll lang="bo" xml:space="preserve">སྤྲིན།</ll>
          <ll lang="br" xml:space="preserve">Koumoul</ll>
          <ll lang="bs" xml:space="preserve">Oblak</ll>
          <ll lang="ca" xml:space="preserve">Núvol</ll>
          <ll lang="chr" xml:space="preserve">ᎤᎶᎩᎸ</ll>
          <ll lang="chy" xml:space="preserve">Vo'e</ll>
          <ll lang="ckb" xml:space="preserve">ھەور</ll>
          <ll lang="co" xml:space="preserve">Nivulu</ll>
          <ll lang="cs" xml:space="preserve">Oblak</ll>
          <ll lang="cy" xml:space="preserve">Cwmwl</ll>
          <ll lang="da" xml:space="preserve">Sky (meteorologi)</ll>
          <ll lang="de" xml:space="preserve">Wolke</ll>
          <ll lang="el" xml:space="preserve">Νέφος</ll>
          <ll lang="eml" xml:space="preserve">Nóvvla</ll>
          <ll lang="eo" xml:space="preserve">Nubo</ll>
          <ll lang="es" xml:space="preserve">Nube</ll>
          <ll lang="et" xml:space="preserve">Pilv</ll>
          <ll lang="eu" xml:space="preserve">Hodei</ll>
          <ll lang="ext" xml:space="preserve">Nuvi</ll>
          <ll lang="fa" xml:space="preserve">ابر</ll>
          <ll lang="fi" xml:space="preserve">Pilvi</ll>
          <ll lang="fiu-vro" xml:space="preserve">Pilv</ll>
          <ll lang="fr" xml:space="preserve">Nuage</ll>
          <ll lang="frr" xml:space="preserve">Swarken</ll>
          <ll lang="fur" xml:space="preserve">Nûl</ll>
          <ll lang="fy" xml:space="preserve">Wolk</ll>
          <ll lang="ga" xml:space="preserve">Scamall</ll>
          <ll lang="gd" xml:space="preserve">Neul</ll>
          <ll lang="gl" xml:space="preserve">Nube</ll>
          <ll lang="gn" xml:space="preserve">Arai</ll>
          <ll lang="gu" xml:space="preserve">વાદળ</ll>
          <ll lang="gv" xml:space="preserve">Bodjal</ll>
          <ll lang="he" xml:space="preserve">ענן</ll>
          <ll lang="hi" xml:space="preserve">बादल</ll>
          <ll lang="hr" xml:space="preserve">Oblaci</ll>
          <ll lang="ht" xml:space="preserve">Nwaj</ll>
          <ll lang="hu" xml:space="preserve">Felhő</ll>
          <ll lang="hy" xml:space="preserve">Ամպ</ll>
          <ll lang="id" xml:space="preserve">Awan</ll>
          <ll lang="io" xml:space="preserve">Nubo</ll>
          <ll lang="is" xml:space="preserve">Ský</ll>
          <ll lang="it" xml:space="preserve">Nuvola</ll>
          <ll lang="iu" xml:space="preserve">ᓄᕗᔭᖅ</ll>
          <ll lang="ja" xml:space="preserve">雲</ll>
          <ll lang="jbo" xml:space="preserve">dilnu</ll>
          <ll lang="jv" xml:space="preserve">Méga</ll>
          <ll lang="ka" xml:space="preserve">ღრუბელი</ll>
          <ll lang="kk" xml:space="preserve">Бұлттар</ll>
          <ll lang="ko" xml:space="preserve">구름</ll>
          <ll lang="krc" xml:space="preserve">Булут</ll>
          <ll lang="ku" xml:space="preserve">Ewr</ll>
          <ll lang="ky" xml:space="preserve">Булут</ll>
          <ll lang="la" xml:space="preserve">Nubes</ll>
          <ll lang="lb" xml:space="preserve">Wollek</ll>
          <ll lang="lij" xml:space="preserve">Nuvia</ll>
          <ll lang="lmo" xml:space="preserve">Niula</ll>
          <ll lang="ln" xml:space="preserve">Lipata</ll>
          <ll lang="lt" xml:space="preserve">Debesis</ll>
          <ll lang="lv" xml:space="preserve">Mākoņi</ll>
          <ll lang="mg" xml:space="preserve">Rahona</ll>
          <ll lang="mk" xml:space="preserve">Облак</ll>
          <ll lang="ml" xml:space="preserve">മേഘം</ll>
          <ll lang="mn" xml:space="preserve">Үүл</ll>
          <ll lang="mr" xml:space="preserve">ढग</ll>
          <ll lang="ms" xml:space="preserve">Awan</ll>
          <ll lang="nah" xml:space="preserve">Mixtli</ll>
          <ll lang="ne" xml:space="preserve">बादल</ll>
          <ll lang="new" xml:space="preserve">सुपाँय्</ll>
          <ll lang="nl" xml:space="preserve">Wolk</ll>
          <ll lang="nn" xml:space="preserve">Sky</ll>
          <ll lang="no" xml:space="preserve">Sky</ll>
          <ll lang="nrm" xml:space="preserve">Nouage</ll>
          <ll lang="nso" xml:space="preserve">Leru</ll>
          <ll lang="oc" xml:space="preserve">Nívol</ll>
          <ll lang="pa" xml:space="preserve">ਬੱਦਲ</ll>
          <ll lang="pap" xml:space="preserve">Nubia</ll>
          <ll lang="pdc" xml:space="preserve">Wolk</ll>
          <ll lang="pl" xml:space="preserve">Chmura</ll>
          <ll lang="pnb" xml:space="preserve">بدل</ll>
          <ll lang="ps" xml:space="preserve">ورېځ</ll>
          <ll lang="pt" xml:space="preserve">Nuvem</ll>
          <ll lang="qu" xml:space="preserve">Phuyu</ll>
          <ll lang="ro" xml:space="preserve">Nor</ll>
          <ll lang="ru" xml:space="preserve">Облака</ll>
          <ll lang="rue" xml:space="preserve">Хмара</ll>
          <ll lang="scn" xml:space="preserve">Nùvula</ll>
          <ll lang="sco" xml:space="preserve">Clood</ll>
          <ll lang="sh" xml:space="preserve">Oblak</ll>
          <ll lang="simple" xml:space="preserve">Cloud</ll>
          <ll lang="sk" xml:space="preserve">Oblak</ll>
          <ll lang="sl" xml:space="preserve">Oblak</ll>
          <ll lang="so" xml:space="preserve">Caad</ll>
          <ll lang="sq" xml:space="preserve">Retë</ll>
          <ll lang="sr" xml:space="preserve">Облак</ll>
          <ll lang="stq" xml:space="preserve">Wulke</ll>
          <ll lang="su" xml:space="preserve">Awan</ll>
          <ll lang="sv" xml:space="preserve">Moln</ll>
          <ll lang="sw" xml:space="preserve">Wingu</ll>
          <ll lang="ta" xml:space="preserve">முகில்</ll>
          <ll lang="te" xml:space="preserve">మేఘం</ll>
          <ll lang="tg" xml:space="preserve">Абр</ll>
          <ll lang="th" xml:space="preserve">เมฆ</ll>
          <ll lang="tl" xml:space="preserve">Ulap</ll>
          <ll lang="tr" xml:space="preserve">Bulut</ll>
          <ll lang="tt" xml:space="preserve">Болытлар</ll>
          <ll lang="uk" xml:space="preserve">Хмара</ll>
          <ll lang="ur" xml:space="preserve">بادل</ll>
          <ll lang="vec" xml:space="preserve">Nùvoła</ll>
          <ll lang="vep" xml:space="preserve">Pil'v</ll>
          <ll lang="vi" xml:space="preserve">Mây</ll>
          <ll lang="wa" xml:space="preserve">Nûlêye</ll>
          <ll lang="war" xml:space="preserve">Dampog</ll>
          <ll lang="wuu" xml:space="preserve">云</ll>
          <ll lang="yi" xml:space="preserve">וואלקן</ll>
          <ll lang="zh" xml:space="preserve">云</ll>
          <ll lang="zh-min-nan" xml:space="preserve">Hûn</ll>
          <ll lang="zh-yue" xml:space="preserve">雲</ll>
        </langlinks>
      </page>
    </pages>
  </query>
</api>"""


sentences_Aquamole_Pot = [
    u'Aquamole Pot is a cave in West Kingsdale, North Yorkshire, England.',
    u'It was originally explored from below by cave divers who had negotiated  of sump passage from Rowten Pot in 1974, to discover a high aven above the river passage.',
    u'History',
    u'',
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

wikitext_Aquamole_Pot_expanded_templates = u"""<table class="infobox vcard" cellspacing="3" style="border-spacing: 3px; width:22em; "><tr><th colspan="2" class="fn org" style="text-align:center; font-size:125%; font-weight:bold; background-color: #e7dcc3;">Aquamole Pot</th></tr><tr class=""><td colspan="2" class="" style="text-align:center; ">
<div class="center"><div style="width:220px; float: none; clear: both; margin-left: auto; margin-right: auto">
<div style="width:220px; padding:0">
<div style="position: relative; ">[[file:Yorkshire Dales National Park UK location map.svg|220px|Map showing the location of Aquamole Pot]]<div style="position: absolute; z-index: 2; top: 49.2%; left: 19.7%; height: 0; width: 0; margin: 0; padding: 0;"><div style="position: relative; text-align: center; left: -4px; top: -4px; width: 8px; font-size: 8px; line-height:0;" title="">[[File:Red pog.svg|8x8px|Aquamole Pot|link=|alt=]]</div></div></div>
<div style="font-size: 90%; padding-top:3px">
</div>
</div>
</div></div></td></tr><tr class=""><th scope="row" style="text-align:left; ">Location</th>
    <td class="" style="">
[[West Kingsdale]], [[North Yorkshire]], [[UK]]</td></tr><tr class=""><th scope="row" style="text-align:left; ">[[Ordnance Survey National Grid|OS grid]]</th>
    <td class="" style="">
<span style="white-space: nowrap">[http://toolserver.org/~rhaworth/os/coor_g.php?pagename=Aquamole_Pot&params=SD+69926+78338_region%3AGB_scale%3A25000 SD 69926 78338]</span>[[Category:Articles with OS grid coordinates]]</td></tr><tr class=""><th scope="row" style="text-align:left; ">Coordinates</th>
    <td class="" style="">
<span class="plainlinks nourlexpansion">[//toolserver.org/~geohack/geohack.php?pagename=Aquamole_Pot&params=54.199909_N_2.46249_W_type:landmark_ <span class="geo-default"><span class="geo-dms" title="Maps, aerial photos, and other data for this location"><span class="latitude">54\xb012\u203200\u2033N</span> <span class="longitude">2\xb027\u203245\u2033W</span></span></span><span class="geo-multi-punct">&#xfeff; / &#xfeff;</span><span class="geo-nondefault"><span class="geo-dec" title="Maps, aerial photos, and other data for this location">54.199909\xb0N 2.46249\xb0W</span><span style="display:none">&#xfeff; / <span class="geo">54.199909; -2.46249</span></span></span>]</span><span style="font-size: small;"><span id="coordinates">[[Geographic coordinate system|Coordinates]]: <span class="plainlinks nourlexpansion">[//toolserver.org/~geohack/geohack.php?pagename=Aquamole_Pot&params=54.199909_N_2.46249_W_type:landmark_ <span class="geo-default"><span class="geo-dms" title="Maps, aerial photos, and other data for this location"><span class="latitude">54\xb012\u203200\u2033N</span> <span class="longitude">2\xb027\u203245\u2033W</span></span></span><span class="geo-multi-punct">&#xfeff; / &#xfeff;</span><span class="geo-nondefault"><span class="geo-dec" title="Maps, aerial photos, and other data for this location">54.199909\xb0N 2.46249\xb0W</span><span style="display:none">&#xfeff; / <span class="geo">54.199909; -2.46249</span></span></span>]</span></span></span></td></tr><tr class=""><th scope="row" style="text-align:left; ">Depth</th>
    <td class="" style="">
113 metres (371 ft)</td></tr><tr class=""><th scope="row" style="text-align:left; ">Length</th>
    <td class="" style="">
142 metres (466 ft)</td></tr><tr class=""><th scope="row" style="text-align:left; ">Discovery</th>
    <td class="" style="">
1974</td></tr><tr class=""><th scope="row" style="text-align:left; ">Geology</th>
    <td class="" style="">
[[Limestone]]</td></tr><tr class=""><th scope="row" style="text-align:left; ">Entrances</th>
    <td class="" style="">
2</td></tr><tr class=""><th scope="row" style="text-align:left; ">Access</th>
    <td class="" style="">
Free</td></tr><tr class=""><th scope="row" style="text-align:left; ">[[Cave survey]]</th>
    <td class="" style="">
[http://cavemaps.org/cavePages/West%20Kingsdale__Aquamole%20Pot.htm cavemaps.org]</td></tr><tr class=""><th scope="row" style="text-align:left; ">[[British Cave Research Association|BRAC]] [[Cave survey#Accuracy|grade]]</th>
    <td class="" style="">
4B</td></tr>
</table>[[Category:Wikipedia cave articles with unreferenced coordinates|Aquamole Pot]]

\'\'\'Aquamole Pot\'\'\' is a cave in West [[Kingsdale]], [[North Yorkshire]], England. It was originally explored from below by cave divers who had negotiated 550 feet (170 m) of [[Sump (cave)|sump]] passage from [[Rowten Pot]] in 1974, to discover a high [[Pitch (ascent/descent)|aven]] above the river passage.<ref>{{cite journal
 | author = Geoff Yeaden
 | year = 1974
 | month = July
 | title = Kingsdale master cave, Yorkshire
 | journal = [[Cave Diving Group|Cave diving group newsletter]]
 | issue = New series No.32
 | pages = page 16\u201318
 }}</ref>

==History==
 
The 130 feet (40 m) aven was scaled in 1980 using poles, ladders and hand bolting kits, and a radio location transmitter placed at the highest point. Having discovered it was 180 feet (55 m) from, and 180 feet (55 m) below [[Jingling Pot]], the aven was renamed Aquamole Aven instead of Jingling Avens.<ref>{{cite journal
 | author = Ian Watson
 | year = 1980
 | month = April
 | title = Kingsdale master cave, Yorkshire, Jingling Avens, Late reports
 | journal = [[Cave Diving Group|Cave diving group newsletter]]
 | issue = New series No.59
 | pages = page 12\u201313
 }}</ref>  

Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to 50 feet (15 m) below the moor. It was finally connected to the surface in June 2002.<ref>{{cite journal
 | author = Rupe Skorupka
 | year = 2002
 | month = October
 | title = A Pot Into Aquamole
 | journal = [[Descent (magazine)]]
 | issn = 0046-0036
 | issue = 168
 | pages = page 20\u201322
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
        map_reftoken_to_urls, wikitext_with_reftokens = \
            get_sents_refs.collect_refs(
                wikitext_Aquamole_Pot_complicated_refs
            )

        self.assertItemsEqual(map_reftoken_to_urls, expect[0])
        self.assertItemsEqual(wikitext_with_reftokens, expect[1])

    def test_strip_wikitext_markup(self):
        expect = """Aquamole Pot is a cave in West Kingsdale, North Yorkshire, England. It was originally explored from below by cave divers who had negotiated 550 feet (170 m) of sump passage from Rowten Pot in 1974, to discover a high aven above the river passage.

History
The 130 feet (40 m) aven was scaled in 1980 using poles, ladders and hand bolting kits, and a radio location transmitter placed at the highest point.  Having discovered it was 180 feet (55 m) from, and 180 feet (55 m) below Jingling Pot, the aven was renamed Aquamole Aven instead of Jingling Avens.

Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to 50 feet (15 m) below the moor.  It was finally connected to the surface in June 2002.""".decode('utf-8').split('\n')[:3]
        actual = get_sents_refs.strip_wikitext_markup(
            wikitext_Aquamole_Pot_expanded_templates
        ).split('\n')[:3]
        self.assertEqual(expect, actual)

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
            [],
            [u'http://www.wildplaces.co.uk/descent/descent168.html',
             u'http://www.wildplaces.co.uk/descent/descent169.html',
             u'http://www.wildplaces.co.uk/descent/descent170.html'],
            [],
            [u'http://www.wildplaces.co.uk/descent/descent168.html',
             u'http://www.wildplaces.co.uk/descent/descent170.html'],
            [],
        ]
        result = get_sents_refs.urls_for_lines(
            sentences_Aquamole_Pot,
            {u'coeref0': [
                    u'http://www.wildplaces.co.uk/descent/descent168.html',
                    u'http://www.wildplaces.co.uk/descent/descent170.html'
                ],
             u'coeref1': [],
             u'coeref2': [
                    u'http://www.wildplaces.co.uk/descent/descent168.html',
                    u'http://www.wildplaces.co.uk/descent/descent169.html'
                ],
            },
            unicode(wiki2plain.Wiki2Plain(wikitext_Aquamole_Pot_complicated_refs_replaced).text)
        )
        actual = [line.urls for line in result]
        self.assertEqual(len(expect), len(actual))
        for i in range(len(expect)):
            self.assertItemsEqual(expect[i], actual[i])


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
        actual = get_sents_refs.extract_urls_from_ref(wikitext, True)
        self.assertEqual(expect, actual)

        expect = [u'https://www.youtube.com/watch?v=cTtzyr5sBkc']
        actual = get_sents_refs.extract_urls_from_ref(wikitext)
        self.assertEqual(expect, actual)

    def test_uncited_and_cited_urls_in_a_ref(self):
        wikitext = u"""unclear,<ref>Willey, David (28 February 2013). [http://www.bbc.co.uk/news/world-europe-21624154 "The day Benedict XVI's papacy ended"], [[BBC News]]. 1 March 2013.</ref> and that many different priorities were at play, making this election difficult to predict.<ref>{{cite web|url=http://www.bbc.co.uk/news/world-europe-21731439 |title=The Vatican: Suspense and intrigue |publisher=BBC |date=1 January 1970 |accessdate=12 March 2013}}</ref> Cardinal [[Cormac Murphy-O'Connor]] remarked laughingly to a BBC presenter that his colleagues have been telling him "Siamo confusi&nbsp;– 'we're confused,'" as there were neither clear blocs nor a front-runner.<ref>{{cite web|last=Ivereigh |first=Austen |url=http://www.osvdailytake.com/2013/03/ivereigh-in-rome-does-cardinal.html |title=OSV Daily Take Blog: Ivereigh in Rome: Does cardinal confusion spell a long conclave? |publisher=Osvdailytake.com |accessdate=12 March 2013}}</ref> blah"""

        expect = [u'http://www.bbc.co.uk/news/world-europe-21731439', u'http://www.osvdailytake.com/2013/03/ivereigh-in-rome-does-cardinal.html']
        actual = get_sents_refs.extract_urls_from_ref(wikitext, True)
        self.assertItemsEqual(expect, actual)

        expect = [
            u'http://www.bbc.co.uk/news/world-europe-21624154',
            u'http://www.bbc.co.uk/news/world-europe-21731439',
            u'http://www.osvdailytake.com/2013/03/ivereigh-in-rome-does-cardinal.html'
        ]
        actual = get_sents_refs.extract_urls_from_ref(wikitext)
        self.assertItemsEqual(expect, actual)


class TestSpanish(unittest.TestCase):

    def test_english_Aquamole_Pot(self):
        cli_argv = ['get_sents_refs.py', '-l', 'en', 'Aquamole Pot']
        result = get_sents_refs.main(cli_argv).split('\n')
        actual = len(result)
        self.assertTrue(actual > 0)

    def test_spanish_Aquamole_Pot(self):
        cli_argv = ['get_sents_refs.py', '-l', 'es', 'Aquamole Pot']
        args = get_sents_refs._handle_args(cli_argv)
        expect = 'es'
        actual = args.language
        self.assertEqual(expect, actual)

    def test_language_en_by_default(self):
        """If the language option is not specified, it should be english"""
        cli_argv = ['get_sents_refs.py', 'Aquamole Pot']
        args = get_sents_refs._handle_args(cli_argv)
        expect = 'en'
        actual = args.language
        self.assertEqual(expect, actual)

    def test_title_for_cloud_es(self):
        """If the language option is not specified, it should be english"""
        english_title = 'Cloud'
        lang = 'es'
        actual = get_sents_refs.translated_title(english_title, lang)
        expect = 'Nube'
        self.assertEqual(expect, actual)

    def test_title_for_chavez_es(self):
        """If the language option is not specified, it should be english"""
        english_title = u'Death_and_state_funeral_of_Hugo_Ch\xe1vez'
        lang = 'es'
        actual = get_sents_refs.translated_title(english_title, lang)
        expect = u'Muerte y funeral de Estado de Hugo Ch\xe1vez'
        self.assertEqual(expect, actual)

    def test_es_peru(self):
        cli_argv = ['get_sents_refs.py', '--quoted', '-l', 'es', '2007_Peru_earthquake']
        actual = len(get_sents_refs.main(cli_argv).split('\n'))
        self.assertTrue(actual > 0)

    def test_title_change_peru_es(self):
        english_title = u'2007_Peru_earthquake'
        lang = 'es'
        actual = get_sents_refs.translated_title(english_title, lang)
        expect = u'Terremoto del Per\xfa de 2007'
        self.assertEqual(expect, actual)

    def test_de_2004_Madrid_train_bombings(self):
        cli_argv = ['get_sents_refs.py', '-l', 'de', '2004_Madrid_train_bombings']
        actual = len(get_sents_refs.main(cli_argv).split('\n'))
        self.assertTrue(actual > 0)

    def test_quoted_arg_en(self):
        cli_argv = ['get_sents_refs.py', '--quoted', 'Death_and_state_funeral_of_Hugo_Ch%C3%A1vez']
        actual = len(get_sents_refs.main(cli_argv).split('\n'))
        self.assertTrue(actual > 0)

    def test_quoted_arg_es(self):
        cli_argv = ['get_sents_refs.py', '--quoted', '-l', 'es', 'Death_and_state_funeral_of_Hugo_Ch%C3%A1vez']
        actual = len(get_sents_refs.main(cli_argv).split('\n'))
        self.assertTrue(actual > 0)

    def test_quoted_arg_exception(self):
        """
        Incorrectly omitting the --quoted option will cause an exception on
        pages like this.
        """
        cli_argv = ['get_sents_refs.py', '-l', 'es', 'Death_and_state_funeral_of_Hugo_Ch%C3%A1vez']
        self.assertRaises(SystemExit, get_sents_refs.main, cli_argv)

    def test_normalize_title_en(self):
        """
        Passing the title Cellulose_plant_conflict_between_Argentina_and_Uruguay should get redirected to 'Uruguay River pulp mill dispute'
        """
        lang = 'en',
        title = u'Cellulose_plant_conflict_between_Argentina_and_Uruguay'

        expect = u'Uruguay River pulp mill dispute'
        actual = get_sents_refs.redirected_title(title)

        self.assertEqual(expect, actual)

    def test_normalize_title_en_specchar(self):
        """
        Passing the title fiancé should get redirected to Engagement.
        """
        lang = 'en',
        title = 'fiancé'.decode('utf-8')

        expect = u'Engagement'
        actual = get_sents_refs.redirected_title(title)

        self.assertEqual(expect, actual)


class TestAquamolePotSentences(unittest.TestCase):

    def setUp(self):
        self.text_no_References = [
            u'Aquamole Pot is a cave in West Kingsdale, North Yorkshire, England.',
            u'It was originally explored from below by cave divers who had negotiated 550 feet (170 m) of sump passage from Rowten Pot in 1974, to discover a high aven above the river passage.',
            u'',
            u'History',
            u'',
            u'The 130 feet (40 m) aven was scaled in 1980 using poles, ladders and hand bolting kits, and a radio location transmitter placed at the highest point.',
            u'Having discovered it was 180 feet (55 m) from, and 180 feet (55 m) below Jingling Pot, the aven was renamed Aquamole Aven instead of Jingling Avens.',
            u'',
            u'Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to 50 feet (15 m) below the moor.',
            u'It was finally connected to the surface in June 2002.',
        ]


    def test_sentences(self):
        expect = self.text_no_References
        actual = get_sents_refs.split_sentences(
            get_sents_refs.strip_wikitext_markup(
                get_sents_refs.truncate_lines_after_match(
                    r'^\s*=*\s*References\s*=*\s*$',
                    get_sents_refs.clean_wikitext(
                        wikitext_Aquamole_Pot_expanded_templates
                    )
                )
            )
        )
        self.assertEqual(expect, actual)

    def test_nltk_split_123(self):
        text = u'1. 2. 3.'
        expect = [
            u'1.',
            u'2.',
            u'3.',
        ]
        actual = get_sents_refs.split_sentences(text)
        self.assertEqual(expect, actual)

    def test_nltk_split_AMP(self):
        text = u'Aquamole Pot is a cave in West Kingsdale, North Yorkshire, England. It was originally explored from below by cave divers who had negotiated  of sump passage from Rowten Pot in 1974, to discover a high aven above the river passage.'
        expect = [
            u'Aquamole Pot is a cave in West Kingsdale, North Yorkshire, England.',
            u'It was originally explored from below by cave divers who had negotiated  of sump passage from Rowten Pot in 1974, to discover a high aven above the river passage.',
        ]
        actual = get_sents_refs.split_sentences(text)
        self.assertEqual(expect, actual)

class TestSimple(unittest.TestCase):

    def setUp(self):
        wikitext = [
            u'Foo.<ref>{{cite journal | url = "http://testurl0"}}</ref>',
            u'',
            u'Bar<ref name="ref 0">{{cite journal | url="http://testurl0"}}</ref>baz.',
            u'',
            u"Hello, world. What's up?",
            u'biz<ref name="ref 0">{{cite journal | url = "http://testurl3"}}</ref>',
            u'<ref name ="ref 1">{{cite journal | url = "http://testurl1"}}</ref>bang',
        ]
        self.wikitext = '\n'.join(wikitext) + '\n'

        self.sentences = [
            u'Foo. ',
            u'',
            u'Bar baz.',
            u'',
            u'Hello, world.',
            u"What's up?",
            u'biz ',
            u' bang',
        ]

        wikitext = [
            u'Foo. coeref0 ',
            u'',
            u'Bar coeref1 baz.',
            u'',
            u"Hello, world. What's up?",
            u'biz coeref1 ',
            u' coeref2 bang',
        ]
        self.wikitext_with_reftokens = u'\n'.join(wikitext) + '\n'

        self.expected_map_reftoken_to_urls = {
            'coeref0': [u'testurl0'],
            'coeref1': [u'testurl0', u'testurl3'],
            'coeref2': [u'testurl1'],
        }

        self.expected_urls_list = [
            [u'testurl0'],
            [],
            [u'testurl0', u'testurl3'],
            [],
            [],
            [],
            [u'testurl0', u'testurl3', u'testurl1'],
            []
        ]

    def test_map_reftoken_to_urls(self):
        self.assertItemsEqual(
            self.expected_map_reftoken_to_urls,
            get_sents_refs.collect_refs(self.wikitext, True)[0]
        )

    def test_wikitext_with_reftokens(self):
        expect = self.wikitext_with_reftokens
        actual = get_sents_refs.collect_refs(self.wikitext)[1]
        self.assertEqual(expect, actual
        )

    def test_urls_list(self):
        result = get_sents_refs.urls_for_lines(
            self.sentences,
            self.expected_map_reftoken_to_urls,
            self.wikitext_with_reftokens
        )

        print(result)
        expect = self.expected_urls_list
        self.assertEqual(len(expect), len(result))
        actual = [line.urls for line in result]
        self.assertEqual(len(expect), len(actual))
        for i in range(len(expect)):
            self.assertItemsEqual(expect[i], actual[i])


class TestFixParagraphBoundaries(unittest.TestCase):
    r"""
    Fix the boundary between paragraphs to two consecutive \n characters.
    """

    def test(self):
        wikitext = '\n'.join([
            '1', '',
            '2', '', '',
            '3', '', '', '',
            '4', '', '', '', '',
        ]) + '\n'

        expect = '\n'.join([
            '1', '',
            '2', '',
            '3', '',
            '4', '',
        ]) + '\n'

        actual = get_sents_refs.fix_paragraph_boundaries(wikitext)

        self.assertEqual(expect, actual)


class TestAMP(unittest.TestCase):

    def test(self):
        mapping = {
            'coeref0': [u'http://www.wildplaces.co.uk/descent/descent168.html']
        }

        wikitext_with_refs = """[[Category:Wikipedia cave articles with unreferenced coordinates|Aquamole Pot]]

'''Aquamole Pot''' is a cave in West [[Kingsdale]], [[North Yorkshire]], England. It was originally explored from below by cave divers who had negotiated 550 feet (170 m) of [[Sump (cave)|sump]] passage from [[Rowten Pot]] in 1974, to discover a high [[Pitch (ascent/descent)|aven]] above the river passage.

==Hístory==

The 130 feet (40 m) aven was scaled in 1980 using poles, ladders and hand bolting kits, and a radio location transmitter placed at the highest point. Having discovered it was 180 feet (55 m) from, and 180 feet (55 m) below [[Jingling Pot]], the aven was renamed Aquamole Aven instead of Jingling Avens.

Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to 50 feet (15 m) below the moor. It was finally connected to the surface in June 2002. coeref0

==References==

""".decode('utf-8')

        sentences = [
            'Aquamole Pot is a cave in West Kingsdale, North Yorkshire, England.',
            'It was originally explored from below by cave divers who had negotiated 550 feet (170 m) of sump passage from Rowten Pot in 1974, to discover a high aven above the river passage.',
            '',
            'Hístory'.decode('utf-8'),
            '',
            'The 130 feet (40 m) aven was scaled in 1980 using poles, ladders and hand bolting kits, and a radio location transmitter placed at the highest point.',
            'Having discovered it was 180 feet (55 m) from, and 180 feet (55 m) below Jingling Pot, the aven was renamed Aquamole Aven instead of Jingling Avens.',
            '',
            'Work restarted in 2000 when divers who were keen on a quick route to the sump beyond, rescaled the avens to a higher point, and radio located a position to 50 feet (15 m) below the moor.',
            'It was finally connected to the surface in June 2002.',
            '',
        ]
        map_reftoken_to_urls = {
            'coeref0': ['http://www.wildplaces.co.uk/descent/descent168.html']
        }

        result = get_sents_refs.urls_for_lines(
            sentences,
            map_reftoken_to_urls,
            get_sents_refs.strip_wikitext_markup(wikitext_with_refs)
        )

        self.assertEqual(
            result[6].urls,
            []
        )

        self.assertEqual(
            result[6].sentence[:6],
            'Having'
        )

        self.assertEqual(
            result[9].urls,
            ['http://www.wildplaces.co.uk/descent/descent168.html']
        )


        def test_clean_wikitext(self):
            wikitext = '1\n  \t\n\n2\n'
            self.assertEqual(
                '1\n\n2\n',
                get_sents_refs.clean_wikitext(wikitext)
            )


class TestWikitextFile(unittest.TestCase):

    def test_remove_file_span_en(self):
        wikitext = (
            ' [[File:Torre Pemex (5).jpg|thumb|right|250px|Torre Pemex at '
            'night]] [[something else]]'
        )
        expect = u'   [[something else]]   '
        actual = get_sents_refs.clean_wikitext(wikitext)
        self.assertEqual(expect, actual)

    def test_remove_file_span_es(self):
        wikitext = (
            ' [[Archivo:Torre Pemex (5).jpg|thumb|right|250px|Torre Pemex at '
            'night]] [[something else]]'
        )
        expect = u'   [[something else]]   '
        actual = get_sents_refs.clean_wikitext(wikitext)
        self.assertEqual(expect, actual)


class TestAllRefUrls(unittest.TestCase):

    def test_basic(self):
        wikitext = '<ref>http://www.excelsior.com.mx/2013/02/01/nacional/882114</ref>'
        expected_refs = {
            'coeref0': [
                'http://www.excelsior.com.mx/2013/02/01/nacional/882114',
            ]
        }
        actual, __ = get_sents_refs.collect_refs(wikitext)
        self.assertItemsEqual(expected_refs, actual)

    def test_extract_urls_from_ref(self):
        reftext = '[http://www.milenio.com/cdb/doc/noticias2011/bbebbb8a6449c0ec124e523f92db4102. Todos los lesionados fueron al Hospital Central de Pemex: Segob]'
        expected_urls = ['http://www.milenio.com/cdb/doc/noticias2011/bbebbb8a6449c0ec124e523f92db4102']
        actual = get_sents_refs.extract_urls_from_ref(reftext)
        self.assertEqual(expected_urls, actual)

    def test_collect_refs(self):
        wikitext = u'El edificio fue desalojado totalmente en los minutos subsecuentes de la explosión, se han confirmado 37 decesos y 126 lesionados.<ref>[http://www.milenio.com/cdb/doc/noticias2011/bbebbb8a6449c0ec124e523f92db4102. Todos los lesionados fueron al Hospital Central de Pemex: Segob]</ref><ref>http://www.eluniversal.com.mx/notas/899908.html</ref> Muchos testigos afirmaron que el edificio se "cimbró" debido a la magnitud de la explosión.<ref>http://www.excelsior.com.mx/2013/02/01/nacional/882177</ref>'
        expected_refs = {
            'coeref0': [
                'http://www.milenio.com/cdb/doc/noticias2011/bbebbb8a6449c0ec124e523f92db4102'
            ],
            'coeref1': [
                'http://www.eluniversal.com.mx/notas/899908.html',
            ],
            'coeref2': [
                'http://www.excelsior.com.mx/2013/02/01/nacional/882177',
            ]
        }
        actual, __ = get_sents_refs.collect_refs(wikitext)
        print(actual)
        self.assertEqual(expected_refs, actual)


class TestStripWikitext(unittest.TestCase):

    def test_simple(self):
        """
        should remove == markup from section headers
        """
        self.assertEqual(
            'Refs',
            get_sents_refs.strip_wikitext_markup('==Refs==')
        )

    def test_last_newline_disappears(self):
        """
        should remove == markup from section headers
        """
        self.assertEqual(
            'last line',
            get_sents_refs.strip_wikitext_markup('last line\n')
        )


class TestSimpleUrlsForLines(unittest.TestCase):

    def setUp(self):
        self.line_urls = get_sents_refs.urls_for_lines(
            ['a'],
            {'coeref0': ['url0']},
            'a coeref0',
        )

    def test_len(self):
        expect = 1
        actual = len(self.line_urls)
        self.assertEqual(expect, actual)

    def test_sentence(self):
        expect = 'a'
        actual = self.line_urls[0].sentence
        self.assertEqual(expect, actual)

    def test_url(self):
        expect = ['url0']
        actual = self.line_urls[0].urls
        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
