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
#                        2019-09-17  14:31

import pytest
from common.xc_auth import getUserHeaders
from conf.sysconfig import UC_DB
from conf.sysconfig import UC_REDIS


# 达令家 auth 鉴权
@pytest.fixture(scope='session')
def dheaders(request):
    headers = getUserHeaders(request.param)
    return headers


@pytest.fixture(scope='session')
def uc_db():
    return UC_DB


@pytest.fixture(scope='session')
def uc_redis():
    return UC_REDIS