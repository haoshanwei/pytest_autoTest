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


    def test_updateShopName(self):
        '''更新用户店铺名称'''
        url = UC_HOST + '/xc_uc/inner/manager/shop/updateShopName.do'
        shopId = 588975
        shopName = ranstr(4)
        params = dict(shopId=shopId, shopName=shopName)
        requests.request('POST', url, params=params)

        res = queryShopById(shopId)
        assert shopName == res['data']['name']


    def test_manager_shop_updateShopIndexImg(self):
        '''/xc_uc/inner/manager/shop/updateShopIndexImg.do'''
        url = UC_HOST + '/xc_uc/inner/manager/shop/updateShopIndexImg.do'
        shopId = 1021
        shopIndexImg = random.choice(
            ["http://img0.daling.com/zin/2018/05/21/17/17/FA163E0BD2F9I5LH1BS0PI3PB40.jpg_200x200.jpg",
             "http://img1.daling.com/zin/2018/05/21/17/17/FA163E0BD2F9I5LH1BS0PI3PB40.jpg_200x200.jpg"])
        params = dict(shopId=shopId, shopIndexImg=shopIndexImg)
        requests.request('POST', url, params=params)

        res = queryShopById(shopId)
        assert shopIndexImg == res['data']['indexImg']


    def test_manager_shop_updateShopImg(self):
        '''/xc_uc/inner/manager/shop/updateShopIndexImg.do'''
        url = UC_HOST + '/xc_uc/inner/manager/shop/updateShopImg.do'
        shopId = 1021
        shopImg = random.choice(
            ["http://img2.daling.com/zin/2018/05/21/17/17/FA163E0BD2F9I5LH1BS0PI3PB40.jpg_200x200.jpg",
             "http://img3.daling.com/zin/2018/05/21/17/17/FA163E0BD2F9I5LH1BS0PI3PB40.jpg_200x200.jpg"])
        params = dict(shopId=shopId, shopImg=shopImg)
        requests.request('POST', url, params=params)

        res = queryShopById(shopId)
        assert shopImg == res['data']['shopImg']


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


    def test_manager_shop_queryMaxId(self, uc_db):
        '''/xc_uc/inner/manager/shop/queryMaxId.do'''
        url = UC_HOST + "/xc_uc/inner/manager/shop/queryMaxId.do"
        res = requests.get(url)

        db_res = uc_db.query("select max(id) as id from t_shop")
        assert 200 == res.status_code
        assert db_res.one().id == res.json()['data']
