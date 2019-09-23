# pytest 框架使用

## 环境安装

- pip install pytest # 基础
- pip install pytest-html # html报告
- pip install allure-pytest # allure 美化报告
- pip install cmp-dict # diff dict
- pip install pytest-xdist # 多线程工具
- pip install requests # http 请求
- pip install records # 数据库
- pip install redis==3.0.0 # redis
- pip install redis-py-cluster # redis cluster
- pip install pyyaml # ymal 文件解析
- pip install pytest-rerunfailures # 失败重试 --reruns count
- install allure
  - mac：brew install allure
  - linux: download 二进制包
  - windows: ……

## 命令

### 简单测试

```shell
# -s 输出 print 信息
pytest -s
```

### 指定类+function

```shell
# 指定文件
pytest -v case/test_ucenterInnerUc.py
# 指定function
pytest -v case/test_ucenterInnerUc.py::test_auth
```

### 模糊匹配 case 名字

```shell
# 指定文件
pytest -k ucenter
```

### 生成pytest-html 报表

```shell
# -n 2 两个线程运行case
# --html 生成的报告
# --self-contained-html 把报告的html + css 合并
pytest -s -n 2 --html=./report/report.html --self-contained-html
```

### 生成 xml 报告

```
pytest -v -s -n 2 --alluredir=./report/xml
```

### 生成allure html报告

```
allure generate report/xml -o report/html --clean
```

## 脚本说明

### 目录结构

- case: 放置case的路径
- common: 一些公用方法
- conf: 基本的配置
- report: 报告产出的位置
- data: 放数据驱动的 yaml 文件

### 文件说明

- .conftest.py: pytest 的fixture 文件，非常中有的文件，对pytest-html 报告一定的优化
- .case/conftest.py: case 专有的一些方法，鉴权、数据库链接开启、redis连接
- .conf/sysconfig.py: 一些基本配置
- .common/make_ddt.py: 从yaml 文件中解析case，生成参数化数据
- data/**.yml 是数据驱动的case 存放地

### yml 说明

#### GET

```yaml
sammary:
    description: 用例描述 # 用例的描述，现在并没有实际的意义
    host: ''  # 自动生产的case，该字段是预留字段。可以把下面case 的hosts 提取出来，url 减少
    name: 用例title  # 用例集合标题，方便查看使用
    proxies: # debug 的时候可以配置上代理，方便用抓包工具查看情况
#      http: "http://127.0.0.1:8888"
testcases:
-   name: /xc_uc/inner/dbinfo/user/queryByMobile.do # case 描述，会在运行后显示在用例结合中
    request: # 请求参数
        headers: # headers 信息
            platform: ios
            version: 1.2.6
        cookies: # cookies 信息，可以没有，也可以把下面的 Cookie1: cookiesValue1 行删掉
          Cookie1: cookiesValue1
        method: GET # 请求方法
        params:
            mobile: '18988888888'
        url: http://a.xc.qa.daling.com/xc_uc/inner/dbinfo/user/queryByMobile.do # 请求接口
    validate: # 返回值。只支持 status_code、expectData 两个参数 发布是状态码 + 返回body
        expectData:
            data:
                appOpenid: null
                appToken: 101411386-17043-4c83af4e-e9b2-431b-8b42-f52280681e6e
                appid: null
                cardNo: null
                certificationYn: 0
                changeInviteCodeTimes: 0
                city: 海淀
                comments: 2018-1-11 vivo测试
                country: CN
                createdDate: 1515466130457
                creatorId: 0
                creatorName: system
                deviceId: 6bab8fd32b6ecf6868688305dfd9622bec42d819
                followerInviteCode: '1117297'
                headimgurl: http://img.daling.com/data/files/mobile/img/dalingjia.jpg
                id: 844354
                inBacklistYn: null
                lastAddressId: 2480
                lastPayerId: null
                loginForbiddenYn: null
                loginToast: null
                maxPayerInfoNum: 20
                maxReceiveAddressNum: 20
                mngSession: null
                mobile: '18988888888'
                modiDate: 1564990364405
                modifierId: null
                modifierName: null
                nickName: 匿名
                openid: null
                originMobile: null
                payPwd: f514664487212287219cdfd6b4a5d01d
                platform: ios
                province: 北京
                realName: vivo达令家
                sessionKey: null
                sex: 1
                showMobileYn: 0
                status: 1
                subscribeTime: null
                subscribeYn: 0
                thirdSession: 101411386-14254-44022ae8-79f2-442e-b2c7-e5bc84933850
                touchAppid: null
                touchOpenid: null
                unionid: null
                unsubscribeTime: null
                userType: 1
                vipRegisterTime: null
                wechatId: null
                wechatIdQrcode: null
            errorMsg: 全部成功
            status: 0
        status_code: 200
-   name: /xc_uc/inner/dbinfo/shop/queryById.do
    request:
        headers:
            Postman-Token: b9831260-0be9-4f28-bf7f-37b3969c17f9
            User-Agent: PostmanRuntime/7.15.2
        method: GET
        params:
            shopId: '76274'
        url: http://alixc.beta.daling.com/xc_uc/inner/dbinfo/shop/queryById.do
    validate:
        expectData:
            data:
                code: '151802218013461120'
                comments: null
                createdDate: 1516615294578
                creatorId: 0
                creatorName: system
                description: 欢迎光临小店
                endDate: 1611244800000
                followerInviteCode: '1164272'
                id: 76274
                indexImg: http://img5.daling.com/zin/2018/05/21/17/17/FA163E0BD2F9I5LH1BS0PI3PB40.jpg_200x200.jpg
                inviteCode: '1164950'
                linkFailureYn: null
                modiDate: null
                modifierId: null
                modifierName: null
                name: 秋秋
                originalFollowerCode: '1164272'
                originalFollowerName: 鑫瑶冻品，绿色磨坊
                ownerId: 498506
                pinkBlockoutYn: 0
                recruitLevel: 1
                salesLevel: 0
                selectedSwitch: null
                shareImg: http://img.cdn.daling.com/data/files/mobile/img/dianpufenxiang.jpg
                shopImg: http://img6.daling.com/zin/2018/06/07/06/35/FA163E0BD2F9I6762QA43C3IA5I.jpg
                sourceSn: '161802218012210833'
                startDate: 1516550400000
                status: 1
                stewardType: 2
            errorMsg: 全部成功
            status: 0
        status_code: 200
```

#### POST

```yaml
sammary:
    description: testcase description
    host: ''
    name: testcase title
    proxies:
      http: 'http://127.0.0.1:8888'
testcases:
-   name: /xc_uc/inner/manager/shop/updateShopName.do
    request:
        data:
            shopId: '588975'
            shopName: A环境
        headers:
            Content-Type: application/x-www-form-urlencoded
            Postman-Token: 31366e41-8d99-4e30-bae1-17d11c0481e7
            User-Agent: PostmanRuntime/7.15.2
        method: POST
        url: http://a.xc.qa.daling.com/xc_uc/inner/manager/shop/updateShopName.do
    validate:
        expectData:
            data:
                message: 店铺名称更新成功!
                success: true
            errorMsg: 全部成功
            status: 0
        status_code: 200
```


#### POST-JSON 情况

```yaml
sammary:
  name: demo
  description: 库存系统APP 接口
  host: ""
  proxies:

testcases:
  - name: APP库存批量查询接口
    request:
      data:
        - sku: 60AUSSD08F0O1
          whPosCode: null
      headers:
        Content-Type: application/json
        Postman-Token: 837d2d67-5cbc-450e-a3f1-b698c308e7c1
        User-Agent: PostmanRuntime/7.15.2
      method: POST
      url: http://alixc.beta.daling.com/stock/app/stock/batchSelectStock
    validate:
      expectData:
        code: 200
        data:
          - sku: 60AUSSD08F0O1
            stock: 10275
            tend: true
            whPosCode: null
        message: 成功
        success: true
      status_code: 200
```