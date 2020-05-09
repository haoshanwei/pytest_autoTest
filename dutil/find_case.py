#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Meng xiangguo <mxgnene01@gmail.com>
#
#              _____               ______
#     ____====  ]OO|_n_n__][.      |    |]
#    [________]_|__|________)<     |MENG|
#     oo    oo  'oo OOOO-| oo\_   ~o~~~o~'
# +--+--+--+--+--+--+--+--+--+--+--+--+--+
#                        2019-10-08  19:44


import os

def findCase(file, yml_file, n=1):
    path = os.path.dirname(file)
    if n > 0:
        n = n - 1
        casepath = findCase(path, yml_file, n)
    else:
        casepath = os.path.join(path, 'data', yml_file)

    return casepath