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

import json
import allure
import pytest
import requests
from dutil.res_diff import res_diff
from conf.sysconfig import UC_HOST
from dutil.find_case import findCase
from dutil.make_ddt import MakeDdt

casepath = findCase(__file__, 'uc_inner_uc.yml', n=2)
test_cases = MakeDdt(casepath).makeData_V2()

class TestUcenterInnerUc():

    @pytest.mark.parametrize("dheaders", ["18901060204"], indirect=True)
    def test_auth(self, dheaders):
        '''用户中心内部鉴权接口'''

        url = UC_HOST + '/xc_uc/inner/uc/auth.do'
        res = requests.get(url, headers=dheaders)
        src_data = {'version': '1.0', 'status': 0, 'errorMsg': '全部成功', 'data': {'realName': '孟祥国', "followerInviteCode": "1089686"}}

        assert {} == res_diff(src_data, res.json())

    @allure.title("{name}")
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData, name",
                             test_cases)
    def test_success(self, method, url, params, data, headers, cookies, proxies, status_code, expectData, name):
        '''/inner/uc'''
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(headers)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(data)), name='请求data', attachment_type=allure.attachment_type.TEXT)

        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())