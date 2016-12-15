import cPickle
from pymarkov import markov
import blogbootstrap.settings as settings

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

def make_text():
    #f = open(settings.BASEDICT, 'r')
    #bulk = ""
    #for i,line in enumerate(f):
    #    bulk += line
    #f.close()
    #markov_dict = markov.train([bulk], 3)
    data = load(settings.BASETEXT)
    out = markov.generate(data, 100, 3, join_char=" ")
    result = out[:1].upper() + out[1:].rstrip() + '.'
    return result