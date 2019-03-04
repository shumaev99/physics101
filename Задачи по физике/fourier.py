import tempfile
import os
import scipy.io.wavfile
from pydub import AudioSegment
import numpy as np

def isprime(x):
    if x < 2:
        return False
    if x == 2:
        return True
    if x%2 == 0:
        return False
    i = 3
    while i*i <= x:
        if x%i == 0:
            return False
        i += 2
    return True

def maxdivisor(x):
    if x <= 1:
       return None
    if x == 1:
       return 1
    t = x
    while t%2 == 0:
        t /= 2
    if t == 1:
        return 2
    i = 3
    while t > 1:
        if i*i > t:
            return t
        while t%i == 0:
            t /= i
        i += 2
    return i

def minimize_maxdivisors(x, margin, termination):
    best, bestval = x, maxdivisor(x) * maxdivisor(x//2 + 1)
    for i in range(min(margin, x - 1)):
        thisval = maxdivisor(x - i) * maxdivisor((x-i)//2 + 1)
        if thisval < bestval:
            bestval = thisval
            best = x - i
        if bestval < termination:
            break
    return (best, bestval)

def find_closest_good(x, maxval, goodvals):
    i = 0
    while i < maxval:
        temp = x - i
        if temp > 0:
            for val in goodvals:
                while temp%val == 0:
                    temp /= val
            if temp == 1:
                return x - i
        i += 1
    return None

def decrease_optimal(x, margin):
    goodvals = [2]
    next = 3
    val = None
    while not val:
        print(goodvals)
        val = find_closest_good(x, margin, goodvals)
        if val:
            temp = val//2 + 1
            print("entered",val,temp)
            for div in goodvals:
                while temp%div == 0:
                    temp /= div
            if temp > 1:
                val = None
        while not isprime(next):
            next += 1
        goodvals.append(next)
        next += 1
    return (val, goodvals)

def beginning_silence(stream):
    i = 0
    while (stream[i] == 0).all():
        i += 1
    return i

gain = lambda f: f

audio = AudioSegment.from_file("daleko.mp3", format="mp3")
fd, path = tempfile.mkstemp()
os.close(fd)
audio.export(path, format = "wav")
rate, data = scipy.io.wavfile.read(path)
os.remove(path)
datatype = data.dtype
delta = data.shape[0] - minimize_maxdivisors(data.shape[0], min(beginning_silence(data), 10000), 500)[0]
data = data[delta:]
fftdata = np.fft.rfft(data, axis=0)
fftdata = gain(fftdata)
outdata = np.fft.irfft(data, axis=0).astype(datatype)
print(outdata[:10])
#fd, path = tempfile.mkstemp()
#os.close(fd)
#scipy.io.wavfile.write(path, rate, outdata)
#outaudio = AudioSegment.from_file(path, format="wav")
#os.remove(path)
#outaudio.export("daleko-new.mp3", format="mp3")
