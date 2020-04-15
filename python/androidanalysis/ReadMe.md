# 单元测试

如何进行单元测试呢？

我要只测 cpu 模块是否成功

我要只测 mem内存 模块是否成功

我要只测 pid 模块是否成功

# 命名规则

1. 模块名一般使用全部小写 增加下划线 如 my_phone
2. 类名第一个字母大写，如果有多个单词，每一个单词的第一个字母大写如 : MyPhone
3. 函数名 ： 小写， 如果有多个单词用下划线隔开 如 my_phone
4. 常量名字一般全大写 增加下划线： MY_PHONE


# 依赖库
[仓库地址](https://pypi.org/)

[参考这里](https://pip.pypa.io/en/stable/reference/pip_install/#pip-install)

可以采用 `pip install -r requirement.txt` 的方式进行安装 

以下是 `requirement.txt` 的写法
```python
#how to use?? just run command below
#pip install -r requirements.txt
# 可以直接指定 依赖库的名称
#six
# 也可以直接指定 依赖库的名称以及版本号
#google-api-python-client>=1.6.7
# 以下会下载 指定的 仓库内容到 本项目里面， -e 表明可供修改
# egg 表明项目名称 subdirectory 表明 setup.py 文件所在的位置，如果不在根目录则需要指定
#-e git+https://github.com/cocodataset/cocoapi#egg=pycocotools&subdirectory=PythonAPI
```
