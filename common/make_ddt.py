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
#                        2019-09-17  23:56

import yaml
import pytest
from conf.sysconfig import UC_HOST

class MakeDdt():
    '''
    为数据驱动准备：可以完全手写代码，对确定不变的信息可以 使用该方式
    输入： yaml 文件路径
    输出：[pytest.param(method, url, params, headers, cookies, proxies, status_code, expectData, id=''),
          pytest.param(method, url, params, headers, cookies, proxies, status_code, expectData, id='')
          ]
    '''

    def __init__(self, file):
        self.file = file


    def fromYmlToDict(self):
        with open(self.file) as f:
            data = yaml.load(f)

        return data


    def makeData(self):
        cases_infos = self.fromYmlToDict()
        testcases = cases_infos.get('testcases')
        sammary = cases_infos.get('sammary')
        caseParams = [pytest.param(
            case.get('request').get('method', 'GET'),
            UC_HOST + case.get('request').get('url', ''),
            case.get('request').get('params', {}),
            case.get('request').get('headers', {}),
            case.get('request').get('cookies', {}),
            sammary.get('proxies', {}),
            case.get('validate').get('status_code', 200),
            case.get('validate').get('expectData', {}),
            id=case.get('name', '接口自动化case')
        )  for case in testcases ]

        return caseParams
