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
from common.res_diff import res_diff
from common.make_ddt import MakeDdt

# 数据准备
casepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'uc_inner_dbinfo_payer.yml')
test_cases = MakeDdt(casepath).makeData()
# 数据准备


class TestUcenterInnerDbInfoPayer():
    '''
    基于 yaml 文件数据的自动化case
    '''
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData",
                             test_cases)
    def test_inner_dbinfo_payer(self, method, url, params, data, headers, cookies, proxies, status_code, expectData):
        '''/inner/dbinfo/payer/ 节点下测试用例'''
        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)

        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())
