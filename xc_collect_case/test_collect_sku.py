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
from conf.sysconfig import HOST
from conf.sysconfig import COLLECT_ONE_SKUS
from conf.sysconfig import COLLECT_TWO_SKUS
from conf.sysconfig import COLLECT_ALL_SKUS

casepath = findCase(__file__, 'getUserCollectSkuList.yml', n=1)
test_cases = MakeDdt(casepath).makeData_V2()

casepath1 = findCase(__file__, 'getUserCollectCategoryList.yml', n=1)
test_cases1 = MakeDdt(casepath1).makeData_V2()

class TestCollectSku():
    '''品牌收藏 SKU 纬度的所有接口'''
    def bCollectedSku(self, headers, sku):
        '''判断商品是否收藏'''
        bCollectedSku_url = HOST + '/xc_collect/userCollect/bCollectedSku.do'
        bres = requests.get(bCollectedSku_url, headers=headers, params={'sku': sku})
        return bres

    @pytest.fixture(scope='session')
    @pytest.mark.parametrize("dheaders", ["15147943808"], indirect=True)
    def batchRemoveSku(self, dheaders):
        '''清空所有sku 的收藏'''
        url = '%s/xc_collect/userCollect/batchRemoveSku.do' % HOST
        skusNos = ','.join(COLLECT_ALL_SKUS)
        res = requests.get(url, headers=dheaders, params={'skuNos': skusNos})
        print(res.json()['data'])
        yield
        pass


    @allure.title("商品添加收藏")
    @allure.description("把所有商品从收藏删除之后，添加两个商品到收藏夹")
    @pytest.mark.parametrize("dheaders", ["15147943808"], indirect=True)
    @pytest.mark.parametrize("sku", COLLECT_ONE_SKUS)
    def test_operateCollectSkuCreate(self, dheaders, sku, batchRemoveSku):
        url = HOST + '/xc_collect/userCollect/operateCollectSku.do'
        params = dict(skuNo=sku, operateType='create')
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url, headers=dheaders, params=params)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)
        bres = self.bCollectedSku(dheaders, sku)
        assert '收藏成功' == res.json()['data']
        assert True == bres.json()['data']


    @allure.title("查询用户是否收藏了商品")
    @allure.description("判断SKU是否在收藏夹中，该case判断存在的情况")
    @pytest.mark.parametrize("dheaders", ["15147943808"], indirect=True)
    def test_bCollectedSkuTrue(self, dheaders):
        url = HOST + '/xc_collect/userCollect/bCollectedSku.do'
        sku = COLLECT_ONE_SKUS[0]
        params = dict(sku=sku)
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url, headers=dheaders, params=params)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)
        assert True == res.json()['data']


    @allure.title("查询用户是否收藏了商品")
    @allure.description("判断SKU是否在收藏夹中，该case判断不存在的情况")
    @pytest.mark.parametrize("dheaders", ["15147943808"], indirect=True)
    def test_bCollectedSkuFalse(self, dheaders):
        url = HOST + '/xc_collect/userCollect/bCollectedSku.do'
        sku = COLLECT_TWO_SKUS[0]
        params = dict(sku=sku)
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url, headers=dheaders, params=params)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)
        assert False == res.json()['data']


    @allure.title("商品取消收藏")
    @allure.description("对在收藏夹中的商品，取消商品的收藏状态")
    @pytest.mark.parametrize("dheaders", ["15147943808"], indirect=True)
    def test_operateCollectSkuDelete(self, dheaders):
        url = HOST + '/xc_collect/userCollect/operateCollectSku.do'
        sku = COLLECT_ONE_SKUS[1]
        params = dict(skuNo=sku, operateType='delete')
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url, headers=dheaders, params=params)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)
        bres = self.bCollectedSku(dheaders, sku)
        assert False == bres.json()['data']


    @allure.title("批量取消商品收藏")
    @allure.description("把罗列的所有商品都从收藏夹中移除")
    @pytest.mark.parametrize("dheaders", ["15147943808"], indirect=True)
    def test_batchRemoveSku(self, dheaders):
        url = HOST + '/xc_collect/userCollect/batchRemoveSku.do'
        skuNos = ','.join(COLLECT_ONE_SKUS)
        sku = COLLECT_ONE_SKUS[0]
        params = dict(skuNos=skuNos)
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url, headers=dheaders, params=params)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)
        bres = self.bCollectedSku(dheaders, sku)
        assert False == bres.json()['data']


    @allure.title("将购物车里的失效商品移入收藏夹")
    @allure.description("将购物车里的失效商品移入收藏夹")
    @pytest.mark.parametrize("dheaders", ["15147943808"], indirect=True)
    def test_collectGoodsFromCart(self, dheaders):
        url = HOST + '/xc_collect/userCollect/collectGoodsFromCart.do'
        skuNos = ','.join(COLLECT_ALL_SKUS)
        sku = COLLECT_TWO_SKUS[0]
        params = dict(skuNos=skuNos)
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url, headers=dheaders, params=params)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)
        bres = self.bCollectedSku(dheaders, sku)
        assert True == bres.json()['data']


    @allure.title("商品运营分类查询")
    @allure.description("商品运营分类查询, 数据准备上有4个分类，该case 运行的时候已经所有商品都已经收藏")
    @pytest.mark.parametrize("dheaders", ["15147943808"], indirect=True)
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData, name",
                             test_cases1)
    def test_getUserCollectCategoryList(self, dheaders, method, url, params, data, headers, cookies, proxies, status_code, expectData, name):
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(dheaders)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(data)), name='请求data', attachment_type=allure.attachment_type.TEXT)

        res = requests.request(method, url, params=params, data=data, headers=dheaders, cookies=cookies, proxies=proxies)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())


    @allure.title("用户收藏列表")
    @allure.description("用户收藏列表，包含了各种促销活动")
    @pytest.mark.parametrize("dheaders", ["15147943808"], indirect=True)
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData, name",
                             test_cases)
    def test_getUserCollectSkulist(self, dheaders, method, url, params, data, headers, cookies, proxies, status_code, expectData, name):
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(dheaders)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(data)), name='请求data', attachment_type=allure.attachment_type.TEXT)

        res = requests.request(method, url, params=params, data=data, headers=dheaders, cookies=cookies, proxies=proxies)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())
