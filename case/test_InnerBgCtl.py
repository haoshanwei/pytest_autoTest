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

import os
import pytest
import requests
from dutil.res_diff import res_diff
from dutil.make_ddt import MakeDdt

casepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'uc_inner_bg_ctl.yml')
test_cases = MakeDdt(casepath).makeData()


class TestUcenterInnerBgCtl():
    '''
    基于 yaml 文件数据的自动化case
    '''
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData",
                             test_cases)
    def test_inner_bg_ctl(self, method, url, params, data, headers, cookies, proxies, status_code, expectData):
        '''/inner/bg/ctl/'''
        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)

        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())
