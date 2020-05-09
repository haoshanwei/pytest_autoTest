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

casepath = findCase(__file__, 'app_order_prepare.yml', n=2)
test_cases = MakeDdt(casepath).makeData_V2()


class TestAppOrderPrepare():
    '''
    基于 yaml 文件数据的自动化case
    '''
    # @pytest.mark.skip('暂时先注释掉该接口')
    @allure.title("{name}")
    @allure.description("订单确认页 接口确认")
    @pytest.mark.parametrize("dheaders", ["13911589054"], indirect=True)
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData, name",
                             test_cases)
    def test_success(self, skus, dheaders, method, url, params, data, headers, cookies, proxies, status_code,
                     expectData, name):
        headers.update(dheaders)
        good = skus[0]
        need_update_param = dict(
            sku=good['sku'],
            prodIds=good['id'],
            sn=good['id'],
            addressId=dheaders.get('addressId'),
            id=dheaders.get('addressId')
        )
        if method.upper() == 'GET':
            params.update(need_update_param)
        else:
            data.update(need_update_param)

        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(dheaders)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(data)), name='请求data', attachment_type=allure.attachment_type.TEXT)

        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)
        # print('返回：%s' % res.json())
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())
