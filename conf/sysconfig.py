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
#                        2019-09-17  22:32

import records

# 单独添加使用
COLLECT_ONE_SKUS = ['XX4FXC6IB8001', 'XX4GDTYV59001']
# 从购物车加入收藏
COLLECT_TWO_SKUS = ['WTKF0FMFLX008', 'WTKF0FMFLX010', 'WTKF0FMFLX013', 'XX4GGIOIB8001', 'XX5D4AGIB8001']
# 全部SKU
COLLECT_ALL_SKUS = COLLECT_ONE_SKUS + COLLECT_TWO_SKUS

COLLECT_ONE_BRAND = ['1451', '1452']

COLLECT_TWO_BRAND = ['1454', '1455', '1456']

COLLECT_ALL_BRAND = COLLECT_ONE_BRAND + COLLECT_TWO_BRAND

HOST = 'http://t.xc.qa.daling.com'

UC_DB = records.Database('postgres://daling_app_rw:1234@Daling@i.pgsql1.qa.daling.com:5410/sbc_shop_db')

UC_HOST = 'http://t.xc.qa.daling.com'