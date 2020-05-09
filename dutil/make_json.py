#!/usr/bin/env python
# -coding: utf-8 -
import json


def MakeJson(bodyparam):
     '''
          将key-value键值对转化为json格式
     '''
     bodyparam = bodyparam.replace("=",":").replace("&","\",\"").replace(':','":"')
     bodyparam = "{\"" +bodyparam + "\"}"
     jsonparam = json.loads(bodyparam)
     return jsonparam