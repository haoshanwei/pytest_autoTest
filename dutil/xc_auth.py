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
from urllib.parse import quote


def getUserHeaders(mobile, uc_db, uc_host):
    try:
        sql = '''SELECT
                    tu.id AS user_id, tuld.device_id, tuld.platform, tuld.app_token,
                    tura.id AS address_id, tura.province, tura.city, tura.district,tura.detail
                FROM
                    t_user_receive_address tura
                    JOIN t_user tu ON tu.id = tura.user_id
                    JOIN t_user_login_device tuld ON tu.id = tuld.user_id
                WHERE
                    tuld.expire_yn = 0 AND tu.mobile = '%s'
                ORDER BY
                    tura.modi_date DESC LIMIT 1;
            ''' % mobile

        dbresq = uc_db.query(sql)
        req = dbresq.all()[0]
        # 准备组装 headers
        ouid = req.user_id
        utoken = req.app_token
        platform = req.platform
        clientid = req.device_id
        province = req.province
        city = req.city
        district = req.district
        detail = req.detail
        addressId = req.address_id

        # 加密user_id
        encryptUrl = '%s/xc_uc/inner/bg/ctl/encrypt_uid.do?uid=%s' % (uc_host, ouid)
        resq = requests.get(encryptUrl).json()
        uid = resq['data']
        headers = dict(uid=uid, utoken=utoken, platform=platform, clientid=clientid,
                       addressId=str(addressId), province=quote(province), city=quote(city), district=quote(district),
                       detail=quote(detail))
    except Exception:
        headers = {}

    return headers


def getUserTouchHeaders(id, uc_db, uc_host):
    try:
        sql = '''SELECT tu.id AS user_id, 'wxtouch' AS platform, tu.third_session
            FROM t_user tu
            WHERE tu.status = 1 AND tu.id = %s
            LIMIT 1;
        ''' % id

        dbresq = uc_db.query(sql)
        req = dbresq.all()[0]
        # 准备组装 headers
        ouid = req.user_id
        utoken = req.third_session
        platform = req.platform

        # 加密user_id
        encryptUrl = '%s/xc_uc/inner/bg/ctl/encrypt_uid.do?uid=%s' % (uc_host, ouid)
        resq = requests.get(encryptUrl).json()
        uid = resq['data']
        headers = dict(uid=uid, utoken=utoken, platform=platform)
    except Exception:
        headers = {}

    return headers


def tetAuth(headers, uc_host):
    url= uc_host + "/xc_sale/shop/detail.do?dlj-from=ok"
    req = requests.get(url=url, headers=headers)
    print(req.json())


def getUid(mobile, uc_db):
    try:
        sql = '''select id from t_user where mobile = '%s'
              '''% mobile
        print('SQL =: '+sql)
        dbresq = uc_db.query(sql)
        req = dbresq.all()[0]
        uid = req.id
    except Exception:
        uid = None

    return uid

def getSendCouponParam(mobile,uc_db):
    try:
        sql = '''select T.id,T.mobile,T.user_type,S.ID shop_id from t_user T,t_shop S where mobile ='%s' and T.follower_invite_code = S.invite_code
              '''% mobile
        print('SQL =: '+sql)
        dbresq = uc_db.query(sql)
        req = dbresq.all()[0]

        userId = req.id
        userMobile = req.mobile
        shopId = req.shop_id
        userType = req.user_type

        params = dict(userId=userId, userMobile=userMobile, shopId=shopId, userType=userType)
    except Exception:
        params = {}

    return params


if __name__ == '__main__':
    headers = getUserHeaders('18988888888')
    tetAuth(headers)
