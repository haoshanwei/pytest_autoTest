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
from dutil.res_diff import res_diff
from conf.sysconfig import UC_HOST
from dutil.find_case import findCase
from dutil.make_ddt import MakeDdt

casepath = findCase(__file__, 'uc_inner_uc.yml', n=2)
test_cases = MakeDdt(casepath).makeData()

class TestUcenterInnerUc():

    @pytest.mark.parametrize("dheaders", ["18901060204"], indirect=True)
    def test_auth(self, dheaders):
        '''用户中心内部鉴权接口'''

        url = UC_HOST + '/xc_uc/inner/uc/auth.do'
        res = requests.get(url, headers=dheaders)
        src_data = {'version': '1.0', 'status': 0, 'errorMsg': '全部成功', 'data': {'realName': '孟祥国', "followerInviteCode": "1089686"}}

        assert {} == res_diff(src_data, res.json())


    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData",
                             test_cases)
    def test_test_success(self, method, url, params, data, headers, cookies, proxies, status_code, expectData):
        '''/inner/uc'''
        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)

        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())