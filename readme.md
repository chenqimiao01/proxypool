# proxypool

简易高效的代理池，提供如下功能：
- 定时抓取免费代理网站，简易可扩展。
- 使用 redis 对代理进行存储并对代理可用性进行排序。
- 定时测试和筛选，剔除不可用代理，留下可用代理。
- 提供代理 API，随机取用测试通过的可用代理

## 使用准备

首先克隆代码并进入 proxypool 文件夹：

```
git clone https://github.com/chenqimiao01/proxypool
cd proxypool
```

然后安装项目依赖包：

```
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