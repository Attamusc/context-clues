#!/usr/bin/env python

# The stripped features will be a list of 42 floating point features with the following
# names:

# amp1mean
# amp1std
# amp1skew
# amp1kurt
# amp1dmean
# amp1dstd
# amp1dskew
# amp1dkurt
# amp10mean
# amp10std
# amp10skew
# amp10kurt
# amp10dmean
# amp10dstd
# amp10dskew
# amp10dkurt
# amp100mean
# amp100std
# amp100skew
# amp100kurt
# amp100dmean
# amp100dstd
# amp100dskew
# amp100dkurt
# amp1000mean
# amp1000std
# amp1000skew
# amp1000kurt
# amp1000dmean
# amp1000dstd
# amp1000dskew
# amp1000dkurt
# power1
# power2
# power3
# power4
# power5
# power6
# power7
# power8
# power9
# power10

import os, subprocess, wave, struct, numpy, csv, sys

def strip(filepath):
    feature_vec1, feature_vec2 = compute_chunk_features(filepath)
    return feature_vec1, feature_vec2
    """
    for path, dirs, files in os.walk('/Users/Atta/Music/iTunes/iTunes\ Media/Music/Deadmau5/4X4=12/'):
        print path
        for f in files:
            #if not f.endswith('.m4a'):
                # Skip any non-M4A files
                #continue
            m4a_file = os.path.join(path, f)
            # Extract the track name (i.e. the file name) plus the names
            # of the two preceding directories. This will be useful
            # later for plotting.
            tail, track = os.path.split(m4a_file)
            tail, dir1 = os.path.split(tail)
            tail, dir2 = os.path.split(tail)
            # Compute features. feature_vec1 and feature_vec2 are lists of floating
            # point numbers representing the statistical features we have extracted
            # from the raw sound data.
            print "looking at '$0'".format(track)
            try:
                feature_vec1, feature_vec2 = compute_chunk_features(m4a_file)
                print feature_vec1
                print feature_vec2
            except:
                continue
    """

# Return feature vectors for two chunks of an M4A file.
def compute_chunk_features(in_file):
    # Extract M4A file to a WAV file
    # Don't have this on a Mac, so instead used afconvert
    #mpg123_command = 'C:\\mpg123-1.12.3-x86-64\\mpg123.exe -w "%s" -r 10000 -m "%s"'
    #afconvert_command = 'afconvert -f \'WAVE\' -d I16@10000 %s %s'
    out_file = '/tmp/output.wav'
    cmd = afconvert_command % (in_file, out_file)
    #print cmd
    temp = run_bash('afconvert -f \'WAVE\' -d I16@10000 /tmp/test.m4a /tmp/output.wav')
    # Read in chunks of data from WAV file
    wav_data1, wav_data2 = read_wav(out_file)
    return features(wav_data1), features(wav_data2)

# Returns two chunks of sound data from wave file.
def read_wav(wav_file):
    w = wave.open(wav_file)
    n = 60 * 10000
    if w.getnframes() < n * 2:
        raise ValueError('Wave file too short')
    frames = w.readframes(n)
    wav_data1 = struct.unpack('%dh' % n*2, frames)
    frames = w.readframes(n)
    wav_data2 = struct.unpack('%dh' % n*2, frames)
    return wav_data1, wav_data2

def features(x):
    x = numpy.array(x)
    f = []

    xs = x
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 10).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 100).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 1000).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    f.extend(fftfeatures(x))
    return f

def moments(x):
    mean = x.mean()
    std = x.var()**0.5
    skewness = ((x - mean)**3).mean() / std**3
    kurtosis = ((x - mean)**4).mean() / std**4
    return [mean, std, skewness, kurtosis]
    
def fftfeatures(wavdata):
    f = numpy.fft.fft(wavdata)
    f = f[2:(f.size / 2 + 1)]
    f = abs(f)
    total_power = f.sum()
    f = numpy.array_split(f, 10)
    return [e.sum() / total_power for e in f]

def run_bash(cmd):
    bash = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = bash.stdout.read().strip()
    return output
