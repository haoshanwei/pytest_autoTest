#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import allure
import random
import pytest
import requests
from dutil.find_case import findCase
from dutil.make_ddt import MakeDdt
from conf.sysconfig import XC_HOST, ORDER_DB
from conf.mysqlconf import sql_update,pgsql_update
from dutil.res_diff import res_diff
from dutil.common import ranstr


casepath = findCase(__file__, 'createOrder.yml', n=2)
test_cases = MakeDdt(casepath).makeData_V2()

casepath_1 = findCase(__file__, 'update_status.yml', n=2)
test_cases_1 = MakeDdt(casepath_1).makeData_V2()

casepath_2 = findCase(__file__, 'batchStockAdd.yml', n=2)
test_cases_2 = MakeDdt(casepath_2).makeData_V2()


class TestAppOrderCreate():
    @allure.title('增加用户的余额')
    @allure.description('通过修改 t_account 表的数据库更新用户的可用余额')
    @pytest.mark.dependency(name="balanceUser")
    def test_balanceUser(self):
        sql = "update t_account set active_money = 10000 where user_id = '{}'".format(844354)
        sql_update(sql)
        url = XC_HOST +'/xc_account/account/freshenCache?userId=844354'
        allure.attach('{0}'.format('GET'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        res = requests.request('get', url)
        allure.attach('{0}'.format(json.dumps(res.text)), name='响应结果', attachment_type=allure.attachment_type.TEXT)
        return res


    @allure.title('校验用户的密码')
    @allure.description('调用xc_paypre接口校验用户的密码正确性')
    @pytest.mark.dependency(name="checkPwd")
    @pytest.mark.parametrize("dheaders", ["18988888888"], indirect=True)
    def test_checkPwd(self,dheaders):
        url = XC_HOST +'/xc_paypre/order/checkPwd.do?payPwd=123456'
        allure.attach('{0}'.format('POST'), name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        res = requests.post(url, headers = dheaders)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)
        #globals()["data"] = res.json().get('data')
        global r
        r = res.json().get('data')

    @allure.title("{name}")
    @allure.description('调库存接口-批量加库存')
    @pytest.mark.parametrize("dheaders", ["18988888888"], indirect=True)
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData, name",
                             test_cases_2)
    def test_batchStockAdd(self, dheaders, method, url, params, data, headers, cookies, proxies, status_code,
                         expectData, name, request):
        headers.update(dheaders)
        data = json.loads(data)
        data["ticketId"] = ranstr(10)
        data = json.dumps(data)
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(dheaders)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(data), name='请求data', attachment_type=allure.attachment_type.TEXT)
        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)
        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())


    @allure.title("{name}")
    @allure.description('普通商品-订单生单接口')
    @pytest.mark.dependency(name="createOrder" ,depends=["checkPwd"])
    @pytest.mark.parametrize("dheaders", ["18988888888"], indirect=True)
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData, name",
                             test_cases)
    def test_createOrder(self, skus, dheaders, method, url, params, data, headers, cookies, proxies, status_code,
                     expectData, name, request):
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

        res = requests.request(method, url, params=params, data=data, headers=dheaders, cookies=cookies, proxies=proxies)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        assert status_code == res.status_code
        try:
            # globals()["orderNo"] = res.json().get('data').get('orderNo')
            # 这个方式也可以去 设置case 的返回的后续使用
            request.config.cache.set("orderNo", res.json().get('data').get('orderNo'))
        except Exception:
            pass
        assert expectData.get('status') == res.json().get('status')


    @allure.title("{name}")
    @allure.description('普通商品-订单生单接口')
    @pytest.mark.dependency(name="updateStatus", depends=["createOrder"])
    @pytest.mark.parametrize("dheaders", ["18988888888"], indirect=True)
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData, name",
                             test_cases_1)
    def test_updateStatus(self,order_db, dheaders, method, url, params, data, headers, cookies, proxies, status_code,
                         expectData, name, request):
        '''更新订单状态'''
        orderNo = request.config.cache.get("orderNo", "002001614444033628")
        if orderNo == "666666":
            pytest.skip('生单失败，跳过')
        headers.update(dheaders)
        need_update_param = dict(
            source_order_no=orderNo
        )
        data.update(need_update_param)

        ORDER_DB.query("update t_sale_order set order_status = 2 where so_no = '{}'".format(orderNo))
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(headers)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(data)), name='请求data', attachment_type=allure.attachment_type.TEXT)

        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        sql = "select order_status from t_sale_order where so_no =" + "'" + orderNo + "'"
        r = pgsql_update(sql)
        if r ==3:
            pass
        else:
            print("订单状态更新失败")
        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())
