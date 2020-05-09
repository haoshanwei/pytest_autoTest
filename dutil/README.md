    1、安装pip命令

    2 安装wheel打包,pip install wheel
    
    3 如果是windows操作系统，pip install twine（上传伺服器）

```
4 当前用户的家目录,新增文件.pypirc,windows在C:\Users\用户\pip\pip.ini配置，内容如下:
[distutils]
index-servers =
 daling

[global]
trusted-host=pypi.douban.com
index-url=https://pypi.douban.com/simple/


[daling]
repository: http://pypi.corp.daling.com
username: 
password: 
```   
 
```
5 打包本地安装
linux：python setup.py local
windows：python setup.py build_py bdist_wheel
         pip install dist/*.whl -U
```        
    6 打包上传
      jenkins工程发布

```
7 本地使用
第一次安装: pip install -i http://pypi.corp.daling.com/simple dutil --trusted-host pypi.corp.daling.com
升级: pip install --upgrade -i http://pypi.corp.daling.com/simple dutil --trusted-host pypi.corp.daling.com


```