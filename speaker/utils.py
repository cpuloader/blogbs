import pickle
import blogbootstrap.settings as settings

import bredbot.markov as markov

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