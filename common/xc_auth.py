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
#                        2019/1/28  下午8:00

import requests
import records
from urllib.parse import quote
from random import choice

sbc_slave = records.Database('postgres://pgsql:oe6Imt570Q6I2ZLd@l-db6.ops.bj2.daling.com:5495/sbc_ucenter_db')


def getUserHeaders(mobile):
    sql = '''SELECT T.id,T.province,T.city,T.district,T.detail,K.*FROM t_user_receive_address T JOIN (
                            SELECT user_id,device_id,platform,app_token FROM t_user_login_device T WHERE T.user_id=(
                            SELECT ID FROM t_user WHERE mobile='%s') AND expire_yn=0) AS K ON T.user_id=K.user_id
                            ''' % mobile

    dbresq = sbc_slave.query(sql)
    resq = dbresq.all()
    req = choice(resq)
    # 准备组装 headers
    ouid = req.user_id
    utoken = req.app_token
    platform = req.platform
    clientid = req.device_id
    province = req.province
    city = req.city
    district = req.district
    detail = req.detail
    addressId = req.id

    # 加密user_id
    encryptUrl = 'http://xc.srv.daling.com/xc_uc/inner/bg/ctl/encrypt_uid.do?uid=%s' % ouid
    resq = requests.get(encryptUrl).json()
    uid = resq['data']
    headers = dict(uid=uid, utoken=utoken, platform=platform, clientid=clientid,
                   addressId=str(addressId), province=quote(province), city=quote(city), district=quote(district),
                   detail=quote(detail))

    return headers


def tetAuth(headers):
    url="https://dalingjia.com/xc_sale/shop/detail.do?dlj-from=ok"
    req = requests.get(url=url, headers=headers)
    print(req.json())


if __name__ == '__main__':
    headers = getUserHeaders('18988888888')
    tetAuth(headers)
