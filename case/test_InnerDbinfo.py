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
#                        2019-09-18  09:53

import pytest
import requests
from cmp_dict import cmp_dict
from common.make_ddt import MakeDdt

user_inner_dbinfo_cases = MakeDdt('data/data.yml').makeData()

class TestUcenterInnerDbInfo():

    '''
    基于 yaml 文件数据的自动化case
    '''
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData",
                             user_inner_dbinfo_cases)
    def test_innerDbInfo(self, method, url, params, data, headers, cookies, proxies, status_code, expectData):
        '''ucenterInnerDbinfo 节点下测试用例'''
        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)

        assert status_code == res.status_code
        assert {} == cmp_dict(expectData, res.json())