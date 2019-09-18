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
- *** install allure 
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

### 文件说明
- .conftest.py: pytest 的fixture 文件，非常中有的文件，对pytest-html 报告一定的优化
- .case/conftest.py: case 专有的一些方法，鉴权、数据库链接开启、redis连接
- .conf/sysconfig.py: 一些基本配置

### 一些语法说明
