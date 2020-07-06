# ShadowSocks

[https://github.com/shadowsocks/shadowsocks](https://github.com/shadowsocks/shadowsocks)

## vultr centos 7 shadowsocks 方案

[注册地址](https://www.vultr.com/?ref=7428701)

[Server Information](https://my.vultr.com/subs/?SUBID=15762015)

ssh root@my_server_ip

`command` + `shift` + `e` 终端右侧显示命令执行时间

```
[root@vultr ~]# ifconfig
-bash: ifconfig: 未找到命令
```

net-tools安装
```
# yum upgrade -y
# yum provides ifconfig     # 检查安装状态
# yum install -y net-tools  # 安装网络工具
# ifconfig -a               # 检查网络工具
```

net-tools安装前后对比

安装前
```
[root@vultr ~]# yum provides ifconfig
已加载插件：fastestmirror
Loading mirror speeds from cached hostfile
 * base: centos.mirror.constant.com
 * epel: epel.mirror.constant.com
 * extras: centos.mirror.constant.com
 * updates: centos.mirror.constant.com
No matches found
```
安装后
```
[root@vultr ~]# yum provides ifconfig
已加载插件：fastestmirror
Loading mirror speeds from cached hostfile
 * base: centos.mirror.constant.com
 * epel: epel.mirror.constant.com
 * extras: centos.mirror.constant.com
 * updates: centos.mirror.constant.com
net-tools-2.0-0.22.20131004git.el7.x86_64 : Basic networking tools
源    ：@base
匹配来源：
文件名    ：/usr/sbin/ifconfig
```

常用工具安装
```
# yum install -y python-pip
# pip install -U pip
# pip -V
# yum install -y vim-enhanced
```

shadowsocks安装
```
# yum install -y git
# git --version
# pip install git+https://github.com/shadowsocks/shadowsocks.git@master
```

服务端配置
```
# cat << EOF > /etc/shadowsocks.json
{
    "server":"my_server_ip",
    "server_port":8388,
    "local_address": "127.0.0.1",
    "local_port":1080,
    "password":"mypassword",
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open": true
}
EOF

# ssserver -c /etc/shadowsocks.json --user nobody -d start    # 启动
# ssserver -c /etc/shadowsocks.json --user nobody -d stop     # 关闭
# less /var/log/shadowsocks.log                               # 日志
```

修改防火墙规则

方式一

vultr 默认是通过系统动态防火墙firewalld控制
```
# firewall-cmd --zone=public --add-port=8282/tcp --permanent
# firewall-cmd --reload
# firewall-cmd --list-ports
```

删除
```
# firewall-cmd --zone=public --remove-port=3128/tcp --permanent
# firewall-cmd --reload
```
3128/tcp 80/tcp 2202/tcp 33080/tcp 5000/tcp 18282/tcp


方式二

也可以先关闭系统firewalld, 然后web管理界面添加防火墙规则，并将规则链接到实例
```
# systemctl stop firewalld      # 关闭系统防火墙
# systemctl disable firewalld   # 取消开机启动
# systemctl status firewalld    # 查看状态
```

查看服务器密码被爆破的情况
```
# grep "Failed password for invalid user" /var/log/secure | awk '{print $13}' | sort | uniq -c | sort -nr | more
```

免密登录设置

创建VPS前可以直接指定SSH密钥登录，如果创建未指定，需要手工操作
```
# ssh-keygen -t rsa
# cp ~/.ssh/id_rsa ~/.ssh/authorized_keys       # 创建authorized_keys(600权限)
# chmod 600 ~/.ssh/authorized_keys
# vi ~/.ssh/authorized_keys                     # 将本地公钥写入服务器
# vi /etc/ssh/sshd_config                       # 修改配置
# systemctl restart sshd
```

配置明细
```
PubkeyAuthentication yes                        # 开启公钥验证
AuthorizedKeysFile .ssh/authorized_keys         # 验证文件路径(默认)

PasswordAuthentication no                       # 禁止密码认证(防止爆破)
```

常用审计命令
```
# lastlog       # 登录日志(/var/log/lastlog)
# last          # 登录成功日志(/var/log/wtmp)
# lastb         # 登录失败日志(/var/log/btmp)
# who           # 当前登录所有用户
```

## vultr

判断服务器是否被墙的方法

1. [http://ping.chinaz.com](http://ping.chinaz.com)
2. [https://tools.ipip.net/ping.php](https://tools.ipip.net/ping.php)

如果被墙，解决方案：

创建快照、创建实例（根据快照类型，选择快照）

ping不通，国内国外都不通，ICMP协议默认没开，安全组规则加上就好了


## 腾讯云

chacha20协议
yum install libsodium
