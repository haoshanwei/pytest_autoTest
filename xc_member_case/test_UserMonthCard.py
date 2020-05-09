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
from dutil.find_case import findCase
from dutil.make_ddt import MakeDdt
from dutil.res_diff import res_diff

from conf.sysconfig import UC_HOST

casepath = findCase(__file__, 'monthcard.yml')
test_cases = MakeDdt(casepath).makeData_V2()


class TestUserMonthCard():
    '''
    基于 yaml 文件数据的自动化case
    '''

    @allure.title("{name}")
    @pytest.mark.parametrize("dheaders", ["13511364630"], indirect=True)
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData, name",
                             test_cases)
    def test_success(self, dheaders, method, url, params, data, headers, cookies, proxies, status_code, expectData, name):
        '''/inner/data/'''
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(dheaders)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(data)), name='请求data', attachment_type=allure.attachment_type.TEXT)
        res = requests.request(method, url, params=params, data=data, headers=dheaders, cookies=cookies, proxies=proxies)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)
        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())

    @allure.title("省钱月卡氛围气泡")
    def test_bubbleDynamic(self):
        url = UC_HOST + '/xc_member/userMonthCard/bubbleDynamic.do'
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)


        res = requests.get(url)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        res = str(res.json()['data'])
        expected_results = "{'nickName': '小七', 'headimgUrl': 'http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIdIwR8uj8eso5gawQO6qvxvG1om9fIrSAVbA2FbyQ4pg5pKS8fw6xNYDSK13tMamdqOBek4x4j3Q/132', 'text': '续费月卡3个月, 已累计开卡6个月'}"
        assert expected_results in res

    @pytest.mark.parametrize("dheaders", ["13911589054"], indirect=True)
    def test_cs(self, dheaders):
        url = 'http://testt.daling.com/xc_member/userMonthCard/getUnusedCoupon.do'
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(dheaders)), name='请求headers', attachment_type=allure.attachment_type.TEXT)

        res = requests.get(url, headers=dheaders)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        res = str(res.json()['data'])
        assert 'couponCode' in res
        assert 'couponName' in res
        assert 'couponDesc' in res
        assert 'couponAmount' in res
        assert 'limitAmount' in res
        assert 'couponId' in res
        assert 'useRange' in res
