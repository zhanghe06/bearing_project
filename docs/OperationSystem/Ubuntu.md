# Ubuntu

## 基础环境配置
```
pip install virtualenv
apt-get install libpango1.0-0
apt-get install libcairo2
apt-get install libpq-dev
pip install -r requirements.txt
```

## 排错
EnvironmentError: mysql_config not found
```
apt-get install libmysqlclient-dev
```

error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
```
apt-get install python-dev
```

## UbuntuServer 系统安装
ubuntu-16.04.2-server-amd64
```
$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 16.04.2 LTS
Release:	16.04
Codename:	xenial
$ lsb_release -c
Codename:	xenial
```

### 服务器安装 OpenSSH 服务
OpenSSH是SSH的替代软件，而且是免费的
```
$ sudo apt-get install openssh-server
$ /etc/init.d/ssh status
```

### 生成密钥对，用户免密登录
（执行以下命令一路回车）
```
$ ssh-keygen -t rsa
```

### 更换国内源
参考：[http://wiki.ubuntu.org.cn/源列表](http://wiki.ubuntu.org.cn/源列表)

```
$ sudo cp /etc/apt/sources.list /etc/apt/sources.list_backup
$ sudo vim /etc/apt/sources.list
```
替换：
```
deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
```
更新：
```
$ sudo apt-get update
```

### docker 安装

准备 add-apt-repository
```
$ sudo apt-get install python-software-properties
$ sudo apt-get install software-properties-common
```

1、Set up the repository
```
$ sudo apt-get -y install \
  apt-transport-https \
  ca-certificates \
  curl
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) \
       stable"
$ sudo apt-get update
```

2、Get Docker CE
```
$ sudo apt-get -y install docker-ce
```

```
$ sudo docker -v
Docker version 17.03.1-ce, build c6d412e
```


### Docker Compose

不翻墙，下载过程极慢
```
$ sudo -i
# curl -L https://github.com/docker/compose/releases/download/1.13.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
# chmod +x /usr/local/bin/docker-compose
$ docker-compose -v
docker-compose version 1.13.0, build 1719ceb
```

compose-file 参考：
https://github.com/docker/docker.github.io/blob/master/compose/compose-file/index.md

```
$ docker-compose build
$ docker-compose up
```

## 防火墙

Ubuntu 18.04 LTS 系统中已经默认附带了 UFW 工具
 
```
# 检查UFW状态
sudo ufw status verbose

# 打开特定端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 打开一组端口
sudo ufw allow 7100:7200/tcp
sudo ufw allow 7100:7200/udp

# 允许访问
sudo ufw allow from 123.123.123.123
sudo ufw allow from 192.168.1.0/24 to any port 3306

# 拒绝访问
sudo ufw deny from 23.34.45.0/24
sudo ufw deny from 23.34.45.0/24 to any port 80

# 查看规则
sudo ufw status numbered

# 删除规则
sudo ufw delete 4               # 通过编号删除
sudo ufw delete allow 8069      # 通过端口删除

# 操作
sudo ufw enable                 # 启用
sudo ufw disable                # 禁用
sudo ufw reset                  # 重置
```
