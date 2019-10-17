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

casepath = findCase(__file__, 'uc_inner_device.yml', n=2)
test_cases = MakeDdt(casepath).makeData()

class TestInnerManagerUser():
    '''
    测试更新与数据库对比的情况
    '''
    def test_updateShopName(self, uc_db):
        '''更新用户店铺头像'''
        url = UC_HOST + '/xc_uc/inner/manager/shop/updateShopName.do'
        shopId = 588975
        shopName = '孟祥国A环境'
        params = dict(shopId=shopId, shopName=shopName)

        requests.request('POST', url, params=params)
        db_shopName = uc_db.query("select name from t_shop where id = {}".format(shopId)).first().name
        assert shopName == db_shopName


    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData",
                             test_cases)
    def test_success(self, method, url, params, data, headers, cookies, proxies, status_code, expectData):
        '''/inner/manager/shop'''
        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)

        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())