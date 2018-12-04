#!/usr/bin/python3

"""
"THE BEER-WARE LICENSE" (Revision 42):
<johannes@the.homestead.dk> wrote this file. As long as you retain this notice
you can do whatever you want with this stuff. If we meet some day, and you
think this stuff is worth it, you can buy me a beer in return
Johannes Lindhart Borresen
"""

# Nice and simple script to suggest abbreviations based on keywords.
# Note! The suggested abbreviated words are NOT guaranteed to be actual
# English words! They *should*, however, be words that you can
# pronounce.

import sys, itertools

words = sys.argv[1:]

print("Suggesting words based on %s" % words)

# The single letters that the abbreviation must be constructed from.
letters = ''.join([x[0] for x in words])

vowels = 'aeiou'
consonants = 'bcdfghjklmnpqrstvwxyz'

digraphs = [
    'sc', 'ng', 'ch', 'gh', 'ph', 'rh', 'sh', 'ti', 'th', 'wh', 'zh', 'ci',
    'wr', 'qu',
    
    'oe', 'oi', 'oy', 'ou', 'ow', 'oa', 'oo',
    'ae', 'ai', 'ay', 'au', 'aw', 'aa', 'ao',
    'ee', 'ei', 'ey', 'eu', 'ew', 'ea',
    'ue', 'ui', 'uy', 'ua', 'uo',
    'ie', 'iu', 'ia', 'io',
    
    'bb', 'dd', 'ff', 'gg', 'll', 'mm', 'nn', 'pp', 'rr', 'ss', 'tt', 'zz'
]
#print('Digraphs:\n%s' % digraphs)

blends = [
    'bl', 'fl', 'cl', 'gl', 'pl', 'sl', 'br', 'cr', 'dr', 'fr', 'gr', 'pr',
    'tr', 'sc', 'sk', 'sm', 'sn', 'sp', 'st', 'sw', 'tw'
]
#print('Blends:\n%s' % blends)

# A word is legal if each of its letters obey the combination rules above
# (digraph or blend) or is vowel followed by a consonant or vice-versa.

def valid_combo(c, n):
    if c + n in digraphs: # Current and next in digraphs.
        return True
    elif c + n in blends: # Current and next in blends.
        return True
    else:
        return True

def valid_triple(triple):
    # Test both tuples as well as all-consonant test.
    if triple[0] in consonants and triple[1] in consonants and triple[2] in consonants and triple != 'sch' and triple != 'tch':
        #print('%s contains all consonants.' % triple)
        return False
    elif not valid_combo(triple[0], triple[1]):
        #print('Tuple %s%s failed in triple %s' % (triple[0], triple[1], triple))
        return False
    elif not valid_combo(triple[1], triple[2]):
        #print('Tuple %s%s failed in triple %s' % (triple[0], triple[1], triple))
        return False
    else:
        return True

def valid_word(word):
    # Test all *triples*
    triples = []
    for n in range(0, len(word)-2):
        triples.append(word[n:n+3])
    #print('Testing triples: %s' % triples)
    for t in triples:
        if not valid_triple(t):
            return False
    # First and last pairs may not be double consonants.
    if word[0:3] != 'sch' and word[0:2] not in (digraphs+blends) and word[0] in consonants and word[1] in consonants:
        print('%s: %s is bad start' % (word, word[0:2]))
        return False
    if word[0:3] not in ('tch', 'sch') and word[-2:] not in (digraphs+blends) and word[-1] in consonants and word[-2] in consonants:
        print('%s: %s is bad end' % (word, word[-2:]))
        return False
    return True
    
def generate_powerset(s):
    if len(s) == 0:
        return []
    l = s.pop()
    subs = generate_powerset(s)
    return subs + [ l+x for x in subs ]

def string_without_letter(s, l):
    lst = list(s)
    lst.pop(s.index(l))
    return ''.join(lst)
    
def generate_combos(s):
    """
    Generates all combinations of length len(s) using *all* components of s.
    Initial step: for each component of s, prepend to all combinations of s
    without that component.
    """
    if len(s) == 1:
        return s
    combos = []
    for l in s:
        combos += [ l + x for x in generate_combos(string_without_letter(s, l))]
    return combos

print(letters)
combos = generate_combos(letters)
valid = []

for c in combos:
    if valid_word(c):
        valid.append(c)
    
for v in valid:
    print(v)