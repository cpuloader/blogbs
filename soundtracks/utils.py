import os, random, math
import string
from subprocess import PIPE, Popen
from tempfile import NamedTemporaryFile

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

MAX_LEN = 2000

def make_peaks(data):
    if not data:
        return None, None
    _, filext = os.path.splitext(data.name)
    filext = filext[1:].lower()
    if filext != 'mp3':
        return None, None
    # DEFAULT_CHUNK_SIZE = 64 * 2 ** 10
    #print(data.size, data.DEFAULT_CHUNK_SIZE, data.size // data.DEFAULT_CHUNK_SIZE)
    step = 10 * data.size // data.DEFAULT_CHUNK_SIZE
    if step > data.DEFAULT_CHUNK_SIZE / 4:
        step = 2 ** 10
    elif step == 0:
        step = 1
    normpeaks = []
    duration = 0.0
    for chunk in data.chunks():
        output = NamedTemporaryFile(mode="rb", delete=False)
        try:
            cmd = ['avconv','-y','-f',filext,'-i','-','-vn','-f','wav',output.name]
            p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            p_out, p_err = p.communicate(chunk)
            if p.returncode != 0:
                raise CouldntDecodeError("Decoding failed. ffmpeg returned error code: {0}\n\nOutput from ffmpeg/avlib:\n\n{1}".format(p.returncode, p_err))
            audio = AudioSegment._from_safe_wav(output)
            maxval = audio.max_possible_amplitude
            duration += audio.duration_seconds
            peaks = audio.get_array_of_samples()[::step]
            part_peaks = [round(abs(x) / maxval, 2) for x in peaks] # normalize absolute peaks
            normpeaks += part_peaks
            #print('peaks length:', len(part_peaks), part_peaks[:10])
        except Exception as err:
            print('Error:', err)
            return None, None
        finally:
            output.close()
            os.remove(output.name)
    #print('final peaks length:', len(normpeaks))
    if len(normpeaks) // MAX_LEN:
        normpeaks = normpeaks[::len(normpeaks) // MAX_LEN] # rebuild peaks
    #print('rebuilt peaks length:', len(normpeaks))
    peaksstring = ",".join([str(x) for x in normpeaks])
    #print('duration:', duration)
    return peaksstring, duration
