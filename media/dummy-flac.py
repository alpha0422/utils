#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# A Librispeech-like synthetic dataset generator
# Author: Wil Kong
# Date: 01/13/2020, Mon

import argparse
import math
import os
import numpy as np
import soundfile as sf

from random import randrange

def parse_args():
    parser = argparse.ArgumentParser(
            description='A Librispeech-like synthetic dataset generator.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--seconds', type=float, default=12.3,
            help='The length of generated .wav file')
    parser.add_argument('--transcript', type=int, default=177,
            help='Length of transcript.')
    parser.add_argument('--rate', type=int, default=16000,
            help='Sample rate.')
    parser.add_argument('--count', type=int, default=16384,
            help='Number of .flac files to generate.')
    parser.add_argument('--path', type=str, default='data/dummy',
            help='Path to store the generated .flac files.')

    return parser.parse_args()

def get_synthetic_dataset(path, seconds, transcript, rate, count):
    # Generate dataset infos
    frames = int(rate * seconds)
    channels = 1
    digits = int(math.log10(count)) + 2
    id1, id2 = randrange(1000), randrange(1000000)
    text = 'A' * transcript
   
    # Create path
    rootpath = os.path.abspath(path)
    flacpath = os.sep.join((rootpath, str(id1), str(id2)))
    if not os.path.exists(rootpath):
        os.makedirs(rootpath)
    if not os.path.exists(flacpath):
        os.makedirs(flacpath)

    trans = os.sep.join((flacpath, '{}-{}.trans.txt'.format(id1, id2)))
    ftran = open(trans, 'w')

    for i in range(count):
        fname = '{}-{}-{num:0{width}}'.format(id1, id2, num=i, width=digits)
        fflac = os.sep.join((flacpath, '{}.flac'.format(fname)))
        sf.write(fflac, np.random.randn(frames, channels), rate, 'PCM_16')
        ftran.write('{} {}\n'.format(fname, text))

    ftran.close()

if __name__ == '__main__':
    args = parse_args()
    get_synthetic_dataset(args.path, args.seconds, args.transcript,
        args.rate, args.count)

