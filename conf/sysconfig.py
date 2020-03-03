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


UC_DB = records.Database('postgres://pgsql:oe6Imt570Q6I2ZLd@l-db1.beta.bj4.daling.com:5495/sbc_shop_db')
UC_REDIS = redis.Redis('redis://a-redis1.qa.bj6.daling.com:6379')
UC_REDIS_CLUSTER = RedisCluster(startup_nodes=[{"host": "a-redis1.qa.bj6.daling.com", "port": 6380},
                                {"host": "a-redis1.qa.bj6.daling.com", "port": 6381},
                                {"host": "a-redis1.qa.bj6.daling.com", "port": 6382},
                                {"host": "a-redis1.qa.bj6.daling.com", "port": 6383},
                                {"host": "a-redis1.qa.bj6.daling.com", "port": 6384},
                                {"host": "a-redis1.qa.bj6.daling.com", "port": 6385}
                                 ])

UC_HOST = 'http://atxc.beta.daling.com'


# PORD
# UC_DB = records.Database('postgres://pgsql:oe6Imt570Q6I2ZLd@l-db6.ops.bj2.daling.com:5495/sbc_ucenter_db')
# UC_HOST = 'http://xc.srv.daling.com'