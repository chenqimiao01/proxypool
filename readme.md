# proxypool

简易高效的代理池，提供如下功能：
- 定时抓取免费代理网站，简易可扩展。
- 使用 redis 对代理进行存储并对代理可用性进行排序。
- 定时测试和筛选，剔除不可用代理，留下可用代理。
- 提供代理 API，随机取用测试通过的可用代理

## 架构

![这是图片](/images/Snipaste_2023-11-20_23-22-36.png "Magic Gardens")

代理池分为四个部分，获取模块、存储模块、检测模块和接口模块。

1. 存储模块使用 Redis 的有序集合，用以代理的去重和状态标识，同时它也是中心模块和基础模块，将其他模块串联起来。
2. 获取模块定时从代理网站获取代理，将获取的代理传递给存储模块，保存到数据库。
3. 检测模块定时通过存储模块获取所有代理，并对其进行检测，根据不同的检测结果对代理设置不同的标识。
4. 接口模块通过 Web API 提供服务接口，其内部还是连接存储模块，获取可用的代理。

## 使用准备

首先克隆代码并进入 `proxypool` 文件夹：

```
git clone https://github.com/chenqimiao01/proxypool
cd proxypool
```

然后安装项目依赖包：

```
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### 安装 redis

#### 本地安装 redis

- Debian/Ubuntu
```
sudo apt-get install redis-server
```

- RHEL/CentOS

```
dnf install redis
```

#### Docker 安装 redis

参考 [菜鸟教程](https://www.runoob.com/docker/docker-tutorial.html)

### 运行

```
python scheduler.py
```

## 使用

成功运行之后可以通过 [http://localhost:5566/getproxy](http://localhost:5566/getproxy) 获取一个随机可用代理。