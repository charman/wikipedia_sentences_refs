# -*- encoding: utf-8 -*-
import get_sents_refs
import re
import unittest
import sys
from bs4 import BeautifulSoup
from string_scanner.scanner import Scanner
#from ddt import ddt, data
import wiki2plain

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
        actual = get_sents_refs.collect_refs(wikitext_Aquamole_Pot_complicated_refs)
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
        actual = [sorted(list) for list in get_sents_refs.urls_for_lines(
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


class TestSpanish(unittest.TestCase):

    def test_english_Aquamole_Pot(self):
        cli_argv = ['get_sents_refs.py', '-l', 'en', 'Aquamole Pot']
        expect = 6
        actual = len(get_sents_refs.main(cli_argv).split('\n'))
        self.assertEqual(expect, actual)

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
        title = u'fianc\xe9'

        expect = u'Engagement'
        actual = get_sents_refs.redirected_title(title)

        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
