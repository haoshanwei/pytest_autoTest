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

import json
import allure
import pytest
import requests
from dutil.res_diff import res_diff
from dutil.find_case import findCase
from dutil.make_ddt import MakeDdt
from conf.sysconfig import ORDER_HOST

casepath = findCase(__file__, 'discountCalculation.yml', n=2)
test_cases = MakeDdt(casepath).makeData_V2()


class TestDiscountCalculation():
    @pytest.mark.skip('2020年05月07日-暂时跳过')
    @allure.title("{name}")
    @allure.description("三个SKU，判断分摊金额")
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData, name",
                             test_cases)
    def test_iscountCalculation(self, method, url, params, data, headers, cookies, proxies, status_code, expectData, name):
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(headers)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(data)), name='请求data', attachment_type=allure.attachment_type.TEXT)
        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        # discountAmountAll = round(sum([i['discountAmount'] for i in res.json()['data']['goods']]), 2)
        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())