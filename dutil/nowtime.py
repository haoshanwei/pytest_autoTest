# -*- coding: UTF-8 -*-
#_auther:zhangxin
#date : 2019/9/26

import time
def nowtime():
    loc_time=time.localtime()
    times=time.strftime('%Y/%m/%d %H:%M:%S',loc_time)
    return times