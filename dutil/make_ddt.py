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
import json
import pytest

class MakeDdt():
    '''
    为数据驱动准备：可以完全手写代码，对确定不变的信息可以 使用该方式
    输入： yaml 文件路径
    输出：[pytest.param(method, url, params, data, headers, cookies, proxies, status_code, expectData, id=''),
          pytest.param(method, url, params, data, headers, cookies, proxies, status_code, expectData, id='')
          ]
    '''

    def __init__(self, file):
        self.file = file


    def fromYmlToDict(self):
        with open(self.file, encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        return data


    def makeData(self):
        cases_infos = self.fromYmlToDict()
        testcases = cases_infos.get('testcases')
        sammary = cases_infos.get('sammary')

        caseParams = []
        for case in testcases:
            method = case.get('request').get('method', 'GET')
            url = sammary.get('host') + case.get('request').get('url', '')
            params = case.get('request').get('params', {})
            data = case.get('request').get('data', {})
            headers = case.get('request').get('headers', {})
            cookies = case.get('request').get('cookies', {})
            proxies = sammary.get('proxies', {})

            status_code = case.get('validate').get('status_code', 200)
            expectData = case.get('validate').get('expectData', '')

            if headers.get('Content-Type', '').startswith('application/json'):
                data = json.dumps(data)
            id = case.get('name', '接口自动化case')

            caseParams.append(pytest.param(method, url, params, data, headers, cookies, proxies, status_code, expectData, id=id))

        return caseParams


    def makeData_V2(self):
        cases_infos = self.fromYmlToDict()
        testcases = cases_infos.get('testcases')
        sammary = cases_infos.get('sammary')
        all_skip = sammary.get('skip', 'False')

        caseParams = []
        if all_skip == 'False':
            for case in testcases:
                skip = case.get('skip', 'False')
                method = case.get('request').get('method', 'GET')
                url = sammary.get('host') + case.get('request').get('url', '')
                params = case.get('request').get('params', {})
                data = case.get('request').get('data', {})
                headers = case.get('request').get('headers', {})
                cookies = case.get('request').get('cookies', {})
                proxies = sammary.get('proxies', {})

                status_code = case.get('validate').get('status_code', 200)
                expectData = case.get('validate').get('expectData', '')

                if headers.get('Content-Type', '').startswith('application/json'):
                    data = json.dumps(data)
                id = case.get('name', '接口自动化case')
                name = id
                if skip == 'False':
                    caseParams.append(pytest.param(method, url, params, data, headers, cookies, proxies, status_code, expectData, name, id=id))
        else:
            # sammary.skip = True && case 中的run == 'True' 的才会运行
            for case in testcases:
                run = case.get('run', 'False')
                method = case.get('request').get('method', 'GET')
                url = sammary.get('host') + case.get('request').get('url', '')
                params = case.get('request').get('params', {})
                data = case.get('request').get('data', {})
                headers = case.get('request').get('headers', {})
                cookies = case.get('request').get('cookies', {})
                proxies = sammary.get('proxies', {})

                status_code = case.get('validate').get('status_code', 200)
                expectData = case.get('validate').get('expectData', '')

                if headers.get('Content-Type', '').startswith('application/json'):
                    data = json.dumps(data)
                id = case.get('name', '接口自动化case')
                name = id
                if run != 'False':
                    caseParams.append(pytest.param(method, url, params, data, headers, cookies, proxies, status_code, expectData, name, id=id))

        return caseParams