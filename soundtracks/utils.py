from pydub import AudioSegment

MAX_LEN = 2000

def make_peaks(data):
    if not data:
        return
    try:
        audio = AudioSegment.from_file(data)
        maxval = audio.max_possible_amplitude
        audiodata = audio.get_array_of_samples()
        if len(audiodata) // MAX_LEN > 2:
            peaks = audiodata[::len(audiodata) // MAX_LEN]
        else:
            peaks = audiodata
        #normpeaks = [round((x + maxval) / (maxval * 2), 2) for x in peaks] # normalize peaks
        normpeaks = [round(abs(x) / maxval, 2) for x in peaks] # normalize absolute peaks
        peaksstring = ",".join([str(x) for x in normpeaks])
    except Exception as err:
        print('Error:', err)
        return
    return peaksstring
