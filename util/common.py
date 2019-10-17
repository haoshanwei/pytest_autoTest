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
#                        2019-10-18  05:32

import random
import requests
from conf.sysconfig import UC_HOST

def ranstr(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    salt = ''
    for i in range(num):
        salt += random.choice(H)

    return salt


def queryUserById(userId):
    query_by_id_url = UC_HOST + '/xc_uc/inner/dbinfo/user/queryById.do?userId=%s' % userId
    return requests.get(query_by_id_url).json()


def queryShopById(shopId):
    query_by_id_url = UC_HOST + '/xc_uc/inner/dbinfo/shop/queryById.do?shopId=%s' % shopId
    return requests.get(query_by_id_url).json()