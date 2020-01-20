#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# A Small Padding Efficiency Calculate Script
# Author: Wil Kong
# Date: 01/20/2020, Mon

# Example:
# 
# import padding_efficiency as padeff
# wav_len, txt_len = padeff.initialize('wav_len_n16', 'txt_len_n16')
# for sig, sig_len, trans, trans_len in train_dataloader:
#     padeff.update(sig_len.tolist(), trans_len.tolist()) 
#     continue
# padeff.post_process()
# padeff.summary()
# padeff.save_np()

from collections import OrderedDict
import numpy as np

__data = OrderedDict()

def initialize(*names):
    global __data
    for name in names:
        __data[name] = []

def update(*lists):
    global __data
    assert len(lists) == len(__data), 'Mis-matched number of lists as initialized!'
    for i, (name, record) in enumerate(__data.items()):
        record.append(lists[i])

def post_process(default=0):
    global __data
    # special process for the last mini-batch
    for name, record in __data.items():
        length = max(map(len, record))
        for j, x in enumerate(record):
            if len(x) < length:
                record[j].extend([default for _ in range(length - len(x))])

def save_np():
    global __data
    for name, record in __data.items():
        np.save('{}.npy'.format(name), np.array(record))

def summary():
    global __data
    for i, (name, record) in enumerate(__data.items()):
        arr = np.array(record)
        eff = arr.sum() / (arr.max(axis=1).sum() * arr.shape[1])
        print('Data {} {}'.format(i, name))
        print('Data shape: {}'.format(repr(arr.shape)))
        print('Total values: {}'.format(arr.sum()))
        print('Padding efficiency: {:.2f}'.format(eff))

