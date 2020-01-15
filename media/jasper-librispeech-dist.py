#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Plot LibriSpeech dataset histogram from Jasper preprocessed JSON file.
# Author: Wil Kong
# Date: 01/15/2020, Wed

import json
import argparse
import os

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser(
            description='A LibriSpeech dataset histogram from Jasper preprocessed JSON file.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('path', type=str,
            help='Path to the directory contains JSON file.')

    return parser.parse_args()

def histogram(data, corpus):
    assert corpus in ['Train', 'Val', 'Test']
    xlabels = ['Audio Length (seconds)', 'Transcript Length']
    for idx, xlabel in enumerate(xlabels):
        # the histogram of the data
        plt.clf()
        x = data[:, idx]
        n, bins, patches = plt.hist(x, 500, facecolor='green', alpha=0.75)
        
        # draw vertical line of average/min/max
        min_ylim, max_ylim = plt.ylim()
        min_xlim, max_xlim = plt.xlim()
        offset = min(0.2, (max_xlim - min_xlim) * 0.1)
        plt.axvline(x.mean(), color='k', linestyle='dashed', linewidth=1)
        plt.text(x.mean() + offset, max_ylim * 0.9, 'Mean: {:.2f}'.format(x.mean()))
        plt.axvline(x.min(), color='k', linestyle='dashed', linewidth=1)
        plt.text(x.min() + offset, max_ylim * 0.9, 'Min: {:.2f}'.format(x.min()))
        plt.axvline(x.max(), color='k', linestyle='dashed', linewidth=1)
        plt.text(x.max() - offset, max_ylim * 0.9, 'Max: {:.2f}'.format(x.max()),
            horizontalalignment='right')

        plt.xlabel(xlabel)
        plt.ylabel('Counts')
        plt.title(r'LibriSpeech {} {} Histogram'.format(corpus, xlabel.split()[0]))
        plt.grid(True)
        
        plt.savefig("librispeech_{}_{}.png".format(corpus.lower(),
            xlabel.split()[0].lower()), dpi=300)

if __name__ == '__main__':
    args = parse_args()

    train_json_files = [
        'librispeech-train-clean-100-wav.json',
        'librispeech-train-clean-360-wav.json',
        'librispeech-train-other-500-wav.json'
    ]
    dev_json_files = [
        'librispeech-dev-clean-wav.json',
        'librispeech-dev-other-wav.json'
    ]
    test_json_files = [
        'librispeech-test-clean-wav.json',
        'librispeech-test-other-wav.json'
    ]

    files = {
        'Train': train_json_files,
        'Val': dev_json_files,
        'Test': test_json_files
    }
    for corpus, alist in files.items(): 
        wav = []
        txt = []
        for afile in alist:
            fpath = os.path.join(args.path, afile)
            fd    = open(fpath, 'r')
            ajson = json.load(fd)
            fd.close()
            for example in ajson:
                wav.append(example["original_duration"])
                txt.append(len(example["transcript"]))

        data = np.column_stack([wav, txt])
        histogram(data, corpus)        

