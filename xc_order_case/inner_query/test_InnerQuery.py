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

casepath = findCase(__file__, 'order_inner_query.yml', n=2)
test_cases = MakeDdt(casepath).makeData_V2()


class TestOrderInnerQuery():
    '''
    基于 yaml 文件数据的自动化case
    '''

    @allure.title("{name}")
    @allure.description("xc_order/inner/order/ 下接口")
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData, name",
                             test_cases)
    def test_inner_query(self, method, url, params, data, headers, cookies, proxies, status_code, expectData, name):
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(headers)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(data)), name='请求data', attachment_type=allure.attachment_type.TEXT)
        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())


    @allure.title("查询最大支付订单ID")
    @allure.description("查询最大订单ID, 和数据库中的已支付订单最大ID比对")
    def test_queryPaidMaxSoId(self, order_db):
        ''''''
        url = ORDER_HOST + "/xc_order/inner/order/query/queryPaidMaxSoId.do"
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        db_res = order_db.query("select id from t_sale_order where pay_date is not null order by pay_date desc limit 1")
        assert 200 == res.status_code
        assert db_res.one().id == res.json()['data']


    @allure.title("查询最大订单ID")
    @allure.description("查询最大订单ID, 和数据库中的最大ID比对")
    def test_queryOrderMaxId(self, order_db):
        url = ORDER_HOST + "/xc_order/inner/order/query/queryOrderMaxId.do"
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        
        res = requests.get(url)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        db_res = order_db.query("select max(id) as id from t_sale_order")
        assert 200 == res.status_code
        assert db_res.one().id == res.json()['data']