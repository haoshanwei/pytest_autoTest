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
#                        2019-09-17  15:19

import pytest
import requests
from cmp_dict import cmp_dict
from conf.sysconfig import UC_HOST


class TestUcenterInnerDbinfo():

    def test_queryByMobile(self):
        '''按照用户Mobile查询用户基本信息'''
        url = UC_HOST + '/xc_uc/inner/dbinfo/user/queryByMobile.do'
        params = dict(mobile='18988888888')
        res = requests.get(url, params=params)
        src_data = {'version': '1.0', 'status': 0, 'errorMsg': '全部成功', 'data': {'realName': 'vivo达令家'}}
        assert {} == cmp_dict(src_data, res.json())


    def test_queryById(self):
        '''按照用户ID查询用户基本信息'''
        url = UC_HOST + '/xc_uc/inner/dbinfo/user/queryById.do'
        params = dict(userId='844354')
        res = requests.get(url, params=params)
        src_data = {'version': '1.0', 'status': 10, 'errorMsg': '全部成功', 'data': {'realName': 'vivo达令家'}}
        assert {} == cmp_dict(src_data, res.json())