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

import redis
import records
from rediscluster import RedisCluster


UC_DB = records.Database('postgres://daling_app_rw:1234@Daling@i.pgsql1.qa.daling.com:5410/sbc_shop_db')
UC_REDIS = redis.Redis('redis://i.redis1.qa.daling.com:6379')
UC_REDIS_CLUSTER = RedisCluster(startup_nodes=[{"host": "i.redisc1.qa.daling.com", "port": 6380},
                                {"host": "i.redisc1.qa.daling.com", "port": 6381},
                                {"host": "i.redisc1.qa.daling.com", "port": 6382},
                                {"host": "i.redisc1.qa.daling.com", "port": 6383},
                                {"host": "i.redisc1.qa.daling.com", "port": 6384},
                                {"host": "i.redisc1.qa.daling.com", "port": 6385}
                                 ])

UC_HOST = 'http://t.xc.qa.daling.com'