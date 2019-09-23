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

#### 普通

```yaml
sammary:
  name: demo
  description: xc_uc/inner/dbinfo 下的所有接口的case集合 # 用例的描述，现在并没有实际的意义
  host: "http://a.xc.qa.daling.com" # 整个接口的运行的域名
  proxies: # debug 的时候可以配置上代理，方便用抓包工具查看情况
    # http: "http://127.0.0.1:8888"

testcases: # cases 集合
  - name: 按照用户ID 查找用户信息 # case 描述，会在运行
    request: # 请求参数
      method: GET # 请求方法
      url: /xc_uc/inner/dbinfo/user/queryById.do # 请求接口
      headers: # headers 信息，可以没有，也可以把下面的 AAA: BBB 行删掉
        AAA: BBB
      cookies: # cookies 信息，可以没有，也可以把下面的 Cookie1: cookiesValue1 行删掉
        Cookie1: cookiesValue1
      params: # 请求参数。 GET、POST 类型的都可以，但是 application/json 类型的 POST 需要把参数列在 下面的json 节点中
        userId: 844354
        test1: value1
      json: {}
    validate: # 返回值。只支持 status_code、expectData 两个参数 发布是状态码 + 返回body
      expectData: {'version': '1.0', 'status': 0, 'errorMsg': '全部成功', 'data': {'realName': 'vivo达令家', "followerInviteCode": "1117297"}}

  - name: 按照用户手机号查找用户信息
    request:
      method: GET
      url: /xc_uc/inner/dbinfo/user/queryByMobile.do
      headers:
        AAA: BBB
      params:
        mobile: '18901060204'
    validate:
      status_code: 200
      expectData: {'version': '1.0', 'status': 0, 'errorMsg': '全部成功', 'data': {'realName': 'mahailin', "followerInviteCode": "1089725"}}
```
