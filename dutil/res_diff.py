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

def res_diff(src_data, dst_data, path='', diff=dict(), sort=False):
    # 这个地方为了解决：pytest.mark.parametrize 多case中一个失败，导致后续case也失败的问题
    if path == '':
        diff = dict()

    if isinstance(src_data, dict):
        for key in src_data:
            newpath = path + '.' + key
            if dst_data is not None and key in dst_data :
                diff = res_diff(src_data[key], dst_data[key], newpath, diff, sort)
            else:
                diff[newpath] = [src_data.get(key), 'not exist is key']
    elif isinstance(src_data, list):
        if len(src_data) == len(dst_data):
            if sort:
                try:
                    tmp = zip(sorted(src_data), sorted(dst_data))
                except Exception:
                    tmp = zip(src_data, dst_data)
            else:
                tmp = zip(src_data, dst_data)
            for k, v in enumerate(tmp):
                diff = res_diff(v[0], v[1], path + '.' + str(k), diff, sort)
        else:
            diff[path] = [src_data, dst_data]
    else:
        if isinstance(src_data, str):
            # 对 img[0-9] 进行 img 替换
            regex = re.compile(r'img(\d?)')
            src_data, number1 = re.subn(regex, 'img', src_data)
            if dst_data:
                dst_data, number2 = re.subn(regex, 'img', dst_data)

        if src_data != dst_data:
            diff[path] = [src_data, dst_data]

    return diff


if __name__ == "__main__":
    xx = {'kkk0':'vvv0', 'kkkk1': [{'c': 'd', 'k2': [{'kk2': 'vv2'}, {'kk3': 'vv3'}]}, {'k3': 'v3'}], 'kkkk2': 'vvvv2'}
    yy = {'kkk0':'vvvv0', 'kkkk1': [{'c': 'd', 'k2': [{'kk2': 'diffvv2'}, {'kk3': 'vv3'}]}, {'k3': None}]}
    diff = res_diff(xx, yy)
    for k, v in diff.items():
        print('key is {} -> value is {}'.format(k, v))