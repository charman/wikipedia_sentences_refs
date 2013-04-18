#!/usr/bin/env python


import re
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..' ))
sys.path.append(os.getcwd())
from scanner import Scanner

scanner = Scanner()

def assert_exception(method, e, args=None):
    if args is None:
      args = tuple()
    try: 
      method(*args)
    except e: return True
    return False
    
  
def test_this():
    
    # run with nothing
    exception_thrown = False
    try: scanner.scan('\s+')
    except: exception_thrown = True
    assert exception_thrown
    
    
    s = 'This is a test string'
    scanner.string = s
    assert scanner.string == s
    assert scanner.bol()
    assert scanner.scan('\w+') == 'This'
    assert scanner.match() == 'This'
    assert scanner.match_len() == 4
    assert scanner.rest() == ' is a test string'
    assert not scanner.scan('\w+') 
    
    assert scanner.scan('\s+')
    assert scanner.match() == ' '
    assert scanner.match_pos() == 4
    assert scanner.match_len() == 1
    assert scanner.pre_match() == 'This', scanner.pre_match()
    assert scanner.rest() == 'is a test string'
    assert scanner.post_match() == 'is a test string'
    pos = scanner.pos
    
    # Check doesn't move us along but it does record matches
    assert scanner.check('\w+')
    assert scanner.match() == 'is'
    assert scanner.match_pos() == 5
    assert scanner.match_len() == 2
    assert scanner.pre_match() == 'This ', scanner.pre_match()
    assert scanner.rest() == 'is a test string'
    assert scanner.post_match() == ' a test string'
    assert scanner.pos == pos
    
    assert scanner.skip('\w+') == 2
    assert scanner.match() == 'is'
    assert scanner.match_pos() == 5
    assert scanner.match_len() == 2
    assert scanner.pre_match() == 'This ', scanner.pre_match()
    assert scanner.rest() == ' a test string'
    assert scanner.post_match() == ' a test string'
    assert scanner.pos == pos+2
    
    pos += 2
    
    assert scanner.peek() == ' '
    assert scanner.peek(2) == ' a'
    assert scanner.get() == ' '
    assert scanner.get(2) == 'a '
    assert scanner.rest() == 'test string'
    
    # matches shouldn't have changed
    assert scanner.match() == 'is'
    assert scanner.match_pos() == 5
    assert scanner.match_len() == 2
    assert scanner.pre_match() == 'This '
    assert scanner.post_match() == ' a test string'
    
    # consumed 3 with get
    assert scanner.pos == pos + 3
    pos+=3
    
    scanner.reset()
    assert scanner.rest() == 'This is a test string', scanner.rest()
    assert scanner.scan('\w') == 'T'
    assert scanner.scan_until('\d') is None
    assert not scanner.matched() 
    
    assert scanner.rest() == 'his is a test string'
    scanner.unscan()
    scanner.unscan()    
    assert scanner.rest() == 'This is a test string'
    
    assert scanner.check_until(r'(?<=\s)is') == 'This is'
    assert scanner.match() == 'This is'
    assert scanner.pre_match() == '', scanner.pre_match()
    assert scanner.post_match() == ' a test string'
    # but we haven't actually moved...
    assert scanner.pos == 0
    assert scanner.rest() == 'This is a test string'
    
    
    assert scanner.scan_until(r'\sa\s') == 'This is a '
    assert scanner.match() == 'This is a '
    assert scanner.pre_match() == ''
    assert scanner.post_match() == 'test string'
    assert scanner.pos == 10
    assert scanner.rest() == 'test string'
    
    assert scanner.skip_until('st') == 4
    
    assert scanner.pos == 14

    
    assert not scanner.eos()
    scanner.terminate()
    assert scanner.eos()
    
    
    scanner.reset()
    assert scanner.scan('(Th)(is)')
    assert scanner.match_groups() == ('Th', 'is'), scanner.match_groups()
    assert scanner.match_groupdict() == {} # no named arguments
    assert scanner.match_group() == 'This'
    assert scanner.match_group(1) == 'Th'
    assert scanner.match_group(2) == 'is'
    
    scanner.unscan()
    # second group won't match
    assert scanner.scan('(th)(e)?', re.I)
    assert scanner.match_groups() == ('Th', None)
    # default value
    assert scanner.match_groups('123') == ('Th', '123')
    
    scanner.unscan()
    
    scanner.scan('(?P<leading>\w+)(?P<whitespace>\s+)(?P<nomatch>\d+)?')
    assert scanner.match_groups() == ('This', ' ', None)
    assert scanner.match_group(0) == 'This '
    
    assert scanner.match_group(1) == 'This'
    assert scanner.match_group('leading') == 'This'    
    assert scanner.match_group(2) == ' '
    assert scanner.match_group('whitespace') == ' '    
    assert scanner.match_group(3) == None
    assert scanner.match_group('nomatch') == None
    
    assert assert_exception(scanner.match_group, IndexError, (5,))
    
    
    assert scanner.match_groupdict() == {'leading': 'This', 'whitespace': ' ',
      'nomatch' : None}
    assert scanner.match_groupdict(False) == {'leading': 'This', 'whitespace': ' ',
      'nomatch' : False}

    
    scanner.reset()
    assert scanner.scan('T') and scanner.matched() == True
    assert not scanner.scan('T') and scanner.matched() == False
    
    assert assert_exception(scanner.match, Exception)
    assert assert_exception(scanner.match_len, Exception)
    assert assert_exception(scanner.match_pos, Exception)
    assert assert_exception(scanner.match_info, Exception)
    assert assert_exception(scanner.match_groups, Exception)
    assert assert_exception(scanner.match_groupdict, Exception)
    assert assert_exception(scanner.match_group, Exception)
    assert assert_exception(scanner.pre_match, Exception)
    assert assert_exception(scanner.post_match, Exception)


    scanner.reset()
    
    assert assert_exception(scanner.match, Exception)
    assert assert_exception(scanner.match_len, Exception)
    assert assert_exception(scanner.match_pos, Exception)
    assert assert_exception(scanner.match_info, Exception)
    assert assert_exception(scanner.match_groups, Exception)
    assert assert_exception(scanner.match_groupdict, Exception)
    assert assert_exception(scanner.match_group, Exception)
    assert assert_exception(scanner.pre_match, Exception)
    assert assert_exception(scanner.post_match, Exception)
    
    assert scanner.scan('A?') == ''
    assert scanner.matched()
    assert scanner.match_len() == 0
    assert scanner.match_pos() == 0
    assert scanner.pre_match() == ''
    assert scanner.post_match() == 'This is a test string'
    
    
    scanner.string = '''line1
line2
line3'''
    assert scanner.bol()
    assert scanner.scan('line1')
    assert not scanner.bol()
    assert scanner.get() == '\n'
    assert scanner.bol()
    assert scanner.scan_until('\d.', re.S) == 'line2\n'    
    assert scanner.bol()
    assert scanner.scan_until('\d') == 'line3'
    assert not scanner.bol()
    assert not scanner.peek()
    assert not scanner.get()    
    assert scanner.eos()
    
    scanner.string = '''line1

line3
line4
line5          \t

line7
line8
line9
line10'''
    assert scanner.bol()
    assert scanner.skip_lines() == 1
    assert scanner.pos == 6
    assert scanner.bol()    
    assert scanner.skip_lines() == 1
    assert scanner.pos == 7
    assert scanner.bol()
    assert not scanner.eol()
    # we're at the start of line 3
    assert scanner.skip_bytes(1) == 1
    assert scanner.skip_bytes(2) == 2
    assert not scanner.bol()
    assert scanner.check('e3')
    assert scanner.skip_lines(2) == 2
    assert scanner.peek(5) == 'line5'
    assert scanner.skip_whitespace() == 0
    assert scanner.skip_bytes(5) == 5
    assert scanner.skip_whitespace(2) == 2
    assert scanner.skip_whitespace(multiline=False) == 9
    assert scanner.check('$', re.M) is not None
    assert scanner.eol()
    assert scanner.skip_whitespace() == 2
    assert scanner.check('line7')
    
    assert scanner.scan( re.compile('line\d') ) == 'line7'
    assert scanner.eol()
    assert assert_exception(scanner.scan, ValueError, (12,))
    assert scanner.skip_lines(100) == 3
    assert scanner.bol()
    assert scanner.peek(6) == 'line10'
    assert scanner.skip_lines() == 0
    
    scanner.reset()
    scanner.string = '0123456789'
    assert scanner.scan_to('3') == '012'
    assert scanner.matched()
    assert scanner.match() == '012'
    assert scanner.pos == 3
    assert scanner.skip_to('5') == 2    
    # match shouldn't change with skip
    assert scanner.match() == '012'
    assert scanner.pos == 5
    assert scanner.check_to('7') == '56'
    assert scanner.pos == 5
    
    scanner.reset()
    scanner.string = '''line1
line2
line3
line4
line5
line6
line7
line8'''

    assert scanner.location() == (1, 1)
    scanner.get()
    assert scanner.location() == (1, 2)
    scanner.get(2)
    assert scanner.location() == (1, 4)    
    assert scanner.skip_lines()
    assert scanner.location() == (2, 1), scanner.location()
    
    scanner.skip_lines(3)
    assert scanner.location() == (5, 1)
    
    # get something in the match history
    scanner.scan('.')    
    pos = scanner.pos    
    matched = (scanner.matched(), scanner.match_pos())
    
    assert scanner.exists('line7')
    assert scanner.pos == pos    
    assert not scanner.exists('line70')
    assert matched ==  (scanner.matched(), scanner.match_pos())
    
    
    

# s.main()
