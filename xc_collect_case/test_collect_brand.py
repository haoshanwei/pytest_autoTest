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
from conf.sysconfig import COLLECT_ONE_BRAND
from conf.sysconfig import COLLECT_TWO_BRAND
from conf.sysconfig import COLLECT_ALL_BRAND

casepath = findCase(__file__, 'getCollectBrandList.yml', n=1)
test_cases = MakeDdt(casepath).makeData_V2()


class TestCollectBrand():
    '''品牌收藏 brand 纬度的所有接口'''
    def isCollectBrand(self, brandId, userId):
        '''判断品牌是否收藏'''
        bCollectedSku_url = HOST + '/xc_collect/userCollect/brand/isCollectBrand.do'
        bres = requests.get(bCollectedSku_url, params={'brandId': brandId, 'userId': userId})
        return bres


    def delCollectBrand(self, brandId, headers):
        '''品牌取消收藏'''
        url = HOST + '/xc_collect/userCollect/brand/delCollectBrand.do'
        params = dict(brandId=brandId)
        res = requests.get(url, headers=headers, params=params)
        return res


    @pytest.fixture()
    @pytest.mark.parametrize("dheaders", ["13911589054"], indirect=True)
    def batchRemoveAllBrand(self, dheaders):
        '''清空所有brand 的收藏'''
        url = HOST + '/xc_collect/userCollect/brand/batchDelCollectBrand.do'
        brandIds = ','.join(COLLECT_ALL_BRAND)
        res = requests.get(url, headers=dheaders, params={'brandIds': brandIds})
        print(res.json()['data'])
        yield
        pass


    @allure.title("品牌收藏")
    @allure.description("把所有准备的品牌加入到收藏夹中")
    @pytest.mark.parametrize("dheaders", ["13911589054"], indirect=True)
    @pytest.mark.parametrize("brandId", COLLECT_ONE_BRAND)
    def test_addCollectBrand(self, dheaders, brandId, batchRemoveAllBrand):
        url = HOST + '/xc_collect/userCollect/brand/addCollectBrand.do'
        params = dict(brandId=brandId)
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url, headers=dheaders, params=params)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        bres = self.isCollectBrand(brandId, 1035)
        assert '收藏成功' == res.json()['data']
        assert 1 == bres.json()['data']


    @allure.title("查询用户是否收藏了品牌")
    @allure.description("判断品牌是否在收藏夹中，该case判断存在的情况")
    def test_isCollectBrandTrue(self):
        url = HOST + '/xc_collect/userCollect/brand/isCollectBrand.do'
        brandId = COLLECT_ONE_BRAND[0]
        params = dict(brandId=brandId, userId=1035)
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url, params=params)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        assert 1 == res.json()['data']


    @allure.title("查询用户是否收藏了品牌")
    @allure.description("判断品牌是否在收藏夹中，该case判断不存在的情况")
    @pytest.mark.parametrize("dheaders", ["13911589054"], indirect=True)
    def test_isCollectBrandFalse(self, dheaders):
        url = HOST + '/xc_collect/userCollect/brand/isCollectBrand.do'
        brandId = COLLECT_TWO_BRAND[1]
        self.delCollectBrand(brandId, dheaders)
        params = dict(brandId=brandId, userId=1035)
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url, params=params)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        assert 0 == res.json()['data']


    @allure.title("品牌取消收藏")
    @allure.description("品牌取消收藏")
    @pytest.mark.parametrize("dheaders", ["13911589054"], indirect=True)
    def test_delCollectBrand(self, dheaders):
        url = HOST + '/xc_collect/userCollect/brand/delCollectBrand.do'
        brandId = COLLECT_ONE_BRAND[1]
        params = dict(brandId=brandId)
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url, headers=dheaders, params=params)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        bres = self.isCollectBrand(brandId, 1035)
        assert 0 == bres.json()['data']


    @allure.title("批量取消品牌收藏")
    @allure.description("批量取消品牌收藏")
    @pytest.mark.parametrize("dheaders", ["13911589054"], indirect=True)
    def test_batchDelCollectBrand(self, dheaders):
        url = HOST + '/xc_collect/userCollect/brand/batchDelCollectBrand.do'
        brandIds = ','.join(COLLECT_ALL_BRAND)
        brandId = COLLECT_ALL_BRAND[0]
        params = {'brandIds': brandIds}
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url, headers=dheaders, params=params)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        bres = self.isCollectBrand(brandId, 1035)
        assert 0 == bres.json()['data']


    @allure.title("品牌收藏-为收藏列表准备")
    @allure.description("品牌收藏-为收藏列表准备")
    @pytest.mark.parametrize("dheaders", ["13911589054"], indirect=True)
    @pytest.mark.parametrize("brandId", COLLECT_ALL_BRAND)
    def test_addCollectBrandForList(self, dheaders, brandId):
        url = HOST + '/xc_collect/userCollect/brand/addCollectBrand.do'
        params = dict(brandId=brandId)
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url, headers=dheaders, params=params)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)
        assert '收藏成功' == res.json()['data']


    @allure.title("品牌收藏列表")
    @allure.description("品牌收藏列表")
    @pytest.mark.parametrize("dheaders", ["13911589054"], indirect=True)
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData, name",
                             test_cases)
    def test_getCollectBrandList(self, dheaders, method, url, params, data, headers, cookies, proxies, status_code, expectData, name):
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(dheaders)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(data)), name='请求data', attachment_type=allure.attachment_type.TEXT)

        res = requests.request(method, url, params=params, data=data, headers=dheaders, cookies=cookies, proxies=proxies)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())
