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
#                        2019-09-20  13:46

import re

def res_diff(src_data, dst_data, path='', diff=dict()):
    if isinstance(src_data, dict):
        for key in src_data:
            newpath = path + '.' + key
            if key in dst_data:
                diff = res_diff(src_data[key], dst_data[key], newpath, diff)
            else:
                diff[newpath] = [src_data.get(key), 'not exist is key']
    elif isinstance(src_data, list):
        for k, v in enumerate(zip(src_data, dst_data)):
            res_diff(v[0], v[1], path + '.' + str(k))
    else:
        if isinstance(src_data, str):
            # 对 img[0-9] 进行 img 替换
            regex = re.compile(r'img(\d?)')
            src_data, number1 = re.subn(regex, 'img', src_data)
            dst_data, number2 = re.subn(regex, 'img', dst_data)

        if src_data != dst_data:
            diff[path] = [src_data, dst_data]

    return diff