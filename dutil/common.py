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
#                        2020-01-16  11:36


import random

def ranstr(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    salt = ''
    for i in range(num):
        salt += random.choice(H)

    return salt


def error_cases(header, param, cookie):
    cases=list()
    if len(header) >= 1:
        for k in except_case(header):
            cases.append({'header': k, 'param':param, 'cookie':cookie})

    if len(param)>=1:
        for k in except_case(param):
            cases.append({'header':header, 'param':k, 'cookie':cookie})

    if len(cookie) >= 1:
        for k in except_case(cookie):
            cases.append({'header':header, 'param':param, 'cookie':k})

    return cases

def except_case(param):
    result = []
    if len(param) < 1:
        return result

    except_string=['', None, "~`!@#$%^&*()_+{}|[]\\:;'><,.?/"]
    # 组装异常字符的用例
    for k, v in param.items():
        t=param.copy()
        t.pop(k)

        # 组装不传某一个参数的用例
        result.append(t.copy())
        for i in except_string:
            t[k] = i
            result.append(t.copy())

    return result