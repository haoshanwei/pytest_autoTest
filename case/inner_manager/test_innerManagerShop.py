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
import random
import requests
from dutil.res_diff import res_diff
from dutil.find_case import findCase
from dutil.make_ddt import MakeDdt
from conf.sysconfig import UC_HOST
from util.common import ranstr, queryUserById, queryShopById

casepath = findCase(__file__, 'uc_inner_manager_shop.yml', n=2)
app_stock_cases = MakeDdt(casepath).makeData()


class TestUcenterInnerManagerShop():

    def test_updateShopName(self):
        '''更新用户店铺名称'''
        url = UC_HOST + '/xc_uc/inner/manager/shop/updateShopName.do'
        shopId = 588975
        shopName = ranstr(4)
        params = dict(shopId=shopId, shopName=shopName)
        requests.request('POST', url, params=params)

        res = queryShopById(shopId)
        assert shopName == res['data']['name']


    def test_updateEncryptPayPwd(self):
        '''更新用户店铺密码'''
        url = UC_HOST + '/xc_uc/inner/manager/user/updateEncryptPayPwd.do'
        userId = 1151
        encryptPayPwd = ranstr(15)
        params = dict(userId=userId, encryptPayPwd=encryptPayPwd)
        requests.request('POST', url, params=params)

        res = queryUserById(userId)
        assert encryptPayPwd == res['data']['payPwd']


    def test_updateLastUsedAddressId(self):
        '''更新用户最后使用的地址id'''
        url = UC_HOST + '/xc_uc/inner/manager/user/updateLastUsedAddressId.do'
        userId = 1050
        addressId = random.choice([491693, 491558, 887013, 2266, 561916])
        params = dict(userId=userId, addressId=addressId)
        requests.request('POST', url, params=params)

        res = queryUserById(userId)
        assert addressId == res['data']['lastAddressId']


    '''
    基于 yaml 文件数据的自动化case
    '''
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData",
                             app_stock_cases)
    def test_success(self, method, url, params, data, headers, cookies, proxies, status_code, expectData):
        '''/inner/manager/shop'''
        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)

        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())
