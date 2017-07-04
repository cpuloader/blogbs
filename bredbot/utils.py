# coding: utf-8

import os, random
import pickle
import requests
import hashlib

import blogbootstrap.settings as settings

from . import markov

def help_text():
    return "Privet! I'm Breditel."

def load(filename):
    data = None
    try:
        fh = open(filename, "rb")
        data = pickle.load(fh)
    except (EnvironmentError, pickle.UnpicklingError) as err:
        print("{0}: file load error: {1}".format(filename, err))
    finally:
        if fh is not None:
            fh.close()
    return data

def add_emojies(out):
    basedir = os.path.split(settings.BASEFILE)[0]
    filename = 'emojis.txt'
    fullpath = os.path.join(basedir, filename)
    emojies = []
    with open(fullpath, 'r', ) as emoj_file:
        for emoj in emoj_file:
            emojies.append(bytes(emoj, "ascii").decode("unicode_escape"))
    for emoj in range(random.randint(0, 3)):
        insert_place = random.randint(0, len(out))
        out.insert(insert_place, random.choice(emojies))
    return out

def make_text(ans_words=[]):
    MAT = False
    MATCHECK = [u'хопа', u'жги']
    #f = open(settings.BASEDICT, 'r')
    #bulk = ""
    #for i,line in enumerate(f):
    #    bulk += line
    #f.close()
    #markov_dict = markov.train([bulk], 2, split_callback=markov.letters)
    for ans_word in ans_words:
        if ans_word.isalpha() and ans_word.lower() in MATCHECK:
            MAT = True
    if not MAT:
        data = load(settings.BASEWORDS)
        maxwordlen = 20
    else:
        data = load(settings.MATWORDS)
        maxwordlen = 30
    length = random.randint(0, 200)
    out = markov.generate(data, length, 2, join_char="")
    out = out.split()

    ''' write emojies in file
    with open(fullpath, 'w', ) as out_file:
        for ans_word in ans_words:
            out_file.write(ans_word.encode('unicode_escape'))
    '''
    for ans_word in ans_words:
        if ans_word.isalpha() and random.randint(0,10) > 6:
            insert_place = random.randint(0, len(out))
            out.insert(insert_place, ans_word.lower())
    i = 0
    j = 0
    signs = u'ьъ'

    for word in out:
        if word[0].isupper():
            j = 0
            endsign = random.choice(['.','.','.','.','?','!'])
            out[i-1] = out[i-1] + endsign
            out[i] = out[i][0] + out[i][1:].lower()
        else:
            out[i] = out[i].lower()
        if word[0].lower() in signs:
            out[i] = word[1:]
        if j > 1 and random.randint(0, 10) > 6:
            out[i-1] = out[i-1] + ','
        if len(word) > maxwordlen:
            if word[maxwordlen] in signs:
                insert_place = maxwordlen + 1
            else:
                insert_place = maxwordlen
            out[i] = word[:maxwordlen] + ' ' + word[insert_place:]
        i = i + 1
        j = j + 1
    if not MAT:
        out = add_emojies(out[:])
    out = " ".join(out)
    result = out[:1].upper() + out[1:].rstrip()
    if result[-1] not in ['.','?','!']:
        result = result[:] + '.'
    return result

def get_picture():
    response = requests.get("https://www.python.org/static/img/python-logo@2x.png", stream=True)
            #proxies={"https": "http://proxy.server:3128"}, )
    if response.status_code == 200:
        basedir = os.path.split(settings.BASEFILE)[0]
        filename = hashlib.sha1(str(random.random())).hexdigest()[:5] + '.png'
        fullpath = os.path.join(basedir, filename)
        with open(fullpath, 'wb') as out_file:
            for chunk in response.iter_content(1024):
                out_file.write(chunk)
    del response
    return fullpath

def show_smile():
    s = [u'\U0001f600', u'\U0001F601', u'\U0001F603', u'\U0001F604',
        u'\U0001F605', u'\U0001F606', u'\U0001F60A', u'\U0001F60B', u'\U0001F60E',
        u'\U0001F60D', u'\U0001F618', u'\U0001F617', u'\U0001F619', u'\U0001F61A']
    out = " ".join(s)
    a = u'\U0001F60D'
    return a#.decode('unicode_escape')