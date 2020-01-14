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
    parser.add_argument('--rate', type=int, default=16000,
            help='Sample rate.')
    parser.add_argument('--count', type=int, default=16384,
            help='Number of .flac files to generate.')
    parser.add_argument('--path', type=str, default='data/dummy',
            help='Path to store the generated .flac files.')

    return parser.parse_args()

def get_synthetic_dataset(path, seconds, rate, count):
    # Generate dataset infos
    frames = int(args.rate * args.seconds)
    channels = 1
    digits = int(math.log10(args.count)) + 2
    id1, id2 = randrange(1000), randrange(1000000)
   
    # Create path
    rootpath = os.path.abspath(args.path)
    flacpath = os.sep.join((rootpath, str(id1), str(id2)))
    if not os.path.exists(rootpath):
        os.makedirs(rootpath)
    if not os.path.exists(flacpath):
        os.makedirs(flacpath)

    trans = os.sep.join((flacpath, '{}-{}.trans.txt'.format(id1, id2)))
    ftran = open(trans, 'w')

    for i in range(args.count):
        fname = '{}-{}-{num:0{width}}'.format(id1, id2, num=i, width=digits)
        fflac = os.sep.join((flacpath, '{}.flac'.format(fname)))
        sf.write(fflac, np.random.randn(frames, channels), args.rate, 'PCM_16')
        ftran.write('{} TEST\n'.format(fname))

    ftran.close()

if __name__ == '__main__':
    args = parse_args()
    get_synthetic_dataset(args.path, args.path, args.rate, args.count)

