# 后端

## TODO

- [ ] setup mysql
- [ ] 配置部署环境
- [ ] [设置Flask的Scret Key](https://dormousehole.readthedocs.io/en/latest/tutorial/factory.html#id2)

## 环境

- `python3.6`
- `venv`
- `nginx`
- `uwsgi`
- `gevent`
- `flask`
- `mysql`

### VirtualEnv

后端部分使用了`venv`虚拟环境，`venv`文件夹放入了`.gitignore`中，因此实际的依赖转存到了`requirements.txt`中，可以使用以下命令讲当前的包写入文件中：

```
pip freeze > requirements.txt
```

然后可以使用此命令安装文件中的依赖：

```
pip install -r requirements.txt
```

若使用`venv`环境，则可以使用以下命令进入环境：

```
source ./venv/bin/activate
```

### Mysql

- 用户：
    - 用户名为`easypass`，密码见Keeweb

## 配置