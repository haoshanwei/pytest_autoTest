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
from dutil.xc_auth import getUserHeaders
from conf.sysconfig import UC_DB
from conf.sysconfig import ORDER_DB
from conf.sysconfig import ORDER_REDIS
from conf.sysconfig import UC_HOST
from conf.sysconfig import CAPTCHA_REDIS


# 达令家 auth 鉴权
@pytest.fixture(scope='session')
def dheaders(request):
    '''
    达令家鉴权信息，通过用户手机号从数据库中组装鉴权信息
    :param request: request.param 手机号
    :return: headers
    '''
    headers = getUserHeaders(request.param, UC_DB, UC_HOST)
    return headers


@pytest.fixture(scope='session')
def order_db():
    '''
    用户中心db连接， 返回 records.Database 实例
    '''
    return ORDER_DB


@pytest.fixture(scope='session')
def order_redis():
    '''
    用户中心redis实例，返回 redis.Redis 实例
    '''
    return ORDER_REDIS


@pytest.fixture(scope='session')
def captcha_redis():
    '''
    用户中心redis实例，返回 redis.Redis 实例
    '''
    return CAPTCHA_REDIS


@pytest.fixture(scope='session')
def skus():
    '''
    可以生单的skus
    '''
    return [
        {"id": 728638, "sku": "W1KAGB0OVB6001", "spu": "1KAGB0O"},
        {"id": 731587, "sku": "WZHGF61I1L001", "spu": "ZHGF61"},
        {"id": 416139, "sku": "XYHF6POI1X001", "spu": "YHF6PO"},
        {"id": 772066, "sku": "XXU5YX9LIWW001", "spu": "XU5YX9L"},
    ]


@pytest.fixture(scope='session')
def virtual_good():
    '''
    普通-虚拟商品生单的sku
    '''
    return {"id": 49874, "sku": "X10VD83TICY001", "spu": "10VD83T"}


@pytest.fixture(scope='session')
def choice_goods():
    '''
    精选生单的skus
    '''
    return [
        {"id": 267942, "sku": "WZHDH93FLX001", "spu": "ZHDH93"},
        {"id": 267945, "sku": "X6ACXQ1ICY001", "spu": "6ACXQ1"}
    ]