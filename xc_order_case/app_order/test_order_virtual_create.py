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
import random
from dutil.find_case import findCase
from dutil.make_ddt import MakeDdt

casepath = findCase(__file__, 'createVirtualOrder.yml', n=2)
test_cases = MakeDdt(casepath).makeData_V2()


class TestAppOrderVirtualCreate():
    @allure.title('普通-虚拟品商品-生单接口')
    @pytest.mark.dependency(name="createOrder")
    @pytest.mark.parametrize("dheaders", ["18988888888"], indirect=True)
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData, name",
                             test_cases)
    def test_createOrder(self, skus, dheaders, method, url, params, data, headers, cookies, proxies, status_code,
                     expectData, name, request):
        '''订单生单接口'''
        headers.update(dheaders)
        good = random.choice(skus)
        need_update_param = dict(
            prodIds=good['id'],
            receiveAddressId=dheaders.get('addressId')
        )
        data.update(need_update_param)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(headers)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(data)), name='请求data', attachment_type=allure.attachment_type.TEXT)

        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        try:
            if res.json().get('status') != 0:
                print('生单失败，商品id 是： %s， 返回结果是： %s' % (good['id'], res.json()))
        except Exception:
            pass

        assert status_code == res.status_code
        try:
            # globals()["orderNo"] = res.json().get('data').get('orderNo')
            # 这个方式也可以去 设置case 的返回的后续使用
            request.config.cache.set("orderNo", res.json().get('data').get('orderNo'))
        except Exception:
            pass
        assert expectData.get('status') == res.json().get('status')


    @allure.title("普通商品-普通品-取消订单")
    @allure.description("普通商品-普通品-取消订单")
    @pytest.mark.dependency(name="cancelOrder", depends=["createOrder"])
    @pytest.mark.parametrize("dheaders", ["18988888888"], indirect=True)
    def test_cancelOrder(self, dheaders, request):
        '''取消订单'''
        orderNo = request.config.cache.get("orderNo", "666666")
        if orderNo == "666666":
            pytest.skip('生单失败，跳过取消订单的操作')
        allure.attach('{0}'.format('POST'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format("https://testt.daling.com/xc_order/order/cancelOrder.do"), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(dheaders)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(orderNo)), name='请求data', attachment_type=allure.attachment_type.TEXT)

        res = requests.request('POST', 'https://testt.daling.com/xc_order/order/cancelOrder.do',
                               data=dict(orderNo=orderNo), headers=dheaders)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        assert 200 == res.status_code
        assert 0 == res.json().get('status')


    @allure.title("普通商品-普通品-删除订单")
    @allure.description("普通商品-普通品-删除订单")
    @pytest.mark.dependency(name="deleteOrder", depends=["createOrder","cancelOrder"])
    @pytest.mark.parametrize("dheaders", ["18988888888"], indirect=True)
    def test_deleteOrder(self, dheaders, request):
        orderNo = request.config.cache.get("orderNo", "666666")
        if orderNo == "666666":
            pytest.skip('生单失败，跳过删除订单的操作')
        allure.attach('{0}'.format('POST'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format("https://testt.daling.com/xc_order/order/deleteOrder.do"), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(dheaders)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(orderNo)), name='请求data', attachment_type=allure.attachment_type.TEXT)

        res = requests.request('POST', 'https://testt.daling.com/xc_order/order/deleteOrder.do',
                               data=dict(orderNo=orderNo), headers=dheaders)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        assert 200 == res.status_code
        assert 0 == res.json().get('status')