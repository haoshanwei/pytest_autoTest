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
import requests
from conf.sysconfig import UC_HOST
from dutil.res_diff import res_diff
from dutil.find_case import findCase
from dutil.make_ddt import MakeDdt

casepath = findCase(__file__, 'uc_inner_invite.yml', n=2)
test_cases = MakeDdt(casepath).makeData()


class TestUcenterInnerInvite():
    '''
    基于 yaml 文件数据的自动化case
    '''
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData",
                             test_cases)
    def test_success(self, method, url, params, data, headers, cookies, proxies, status_code, expectData):
        '''/inner/invite'''
        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)

        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())


    def test_invite_queryMaxId(self, uc_db):
        '''/xc_uc/inner/invite/queryMaxId.do'''
        url = UC_HOST + "/xc_uc/inner/invite/queryMaxId.do"
        res = requests.get(url)

        db_res = uc_db.query("select max(id) as id from t_user_free_invite_record")
        assert 200 == res.status_code
        assert db_res.one().id == res.json()['data']