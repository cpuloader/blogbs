# coding: utf-8
from pymarkov import markov
import random
import cPickle

import blogbootstrap.settings as settings

def help_text():
    return "Privet! I'm Breditel."

def load(filename):
    data = None
    try:
        fh = open(filename, "rb")
        data = cPickle.load(fh)
    except (EnvironmentError, cPickle.UnpicklingError) as err:
        raise LoadError(str(err))
    finally:
        if fh is not None:
            fh.close()
    return data

def make_text(ans_word=None):
    #f = open(settings.BASEDICT, 'r')
    #bulk = ""
    #for i,line in enumerate(f):
    #    bulk += line
    #f.close()
    #markov_dict = markov.train([bulk], 2, split_callback=markov.letters)
    data = load(settings.BASEWORDS)
    length = random.choice(xrange(0,200))
    out = markov.generate(data, length, 2, join_char="")
    out = out.split()
    if ans_word:
        insert_place = random.choice(xrange(1,len(out)))
        out.insert(insert_place, ans_word) 
    i = 0
    j = 0
    signs = u'ьъ'
    for word in out:
        if word[0].isupper():
            j = 0
            endsign = random.choice(['.','.','.','.','?','!'])
            out[i-1] = out[i-1] + endsign
            out[i] = out[i][0] + out[i][1:].lower()
        if word[0].lower() in signs:
            out[i] = word[1:]
        if j > 1 and random.choice(xrange(0,10)) > 5:
            out[i-1] = out[i-1] + ','
        #if len(word) > 10:
        #    out[i] = word[:len(word) / 2] + ' ' + word[len(word) / 2:]
        i = i + 1
        j = j + 1
    out = " ".join(out)
    result = out[:1].upper() + out[1:].rstrip()
    if result[-1] not in ['.','?','!']:
        result = result[:] + '.'
    return result