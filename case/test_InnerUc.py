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
#                        2019-09-17  15:19

import pytest
import requests
from cmp_dict import cmp_dict
from conf.sysconfig import UC_HOST


class TestUcenterInnerUc():

    @pytest.mark.parametrize("dheaders", ["18901060204"], indirect=True)
    def test_auth(self, dheaders):
        '''用户中心内部鉴权接口'''

        url = UC_HOST + '/xc_uc/inner/uc/auth.do'
        res = requests.get(url, headers=dheaders)
        src_data = {'version': '1.0', 'status': 0, 'errorMsg': '全部成功', 'data': {'realName': 'mahailin', "followerInviteCode": "1089725"}}

        assert {} == cmp_dict(src_data, res.json())
