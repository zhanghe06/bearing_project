# LDAP

轻型目录访问协议 (Lightweight Directory Access Protocol)

首先LDAP是一种通讯协议，LDAP支持TCP/IP。
协议就是标准，并且是抽象的。
在这套标准下，AD（Active Directory）是微软出的一套实现。

[https://www.python-ldap.org/en/python-ldap-3.3.0/installing.html](https://www.python-ldap.org/en/python-ldap-3.3.0/installing.html)

Debian/Ubuntu:
```
apt-get install python3-dev python2.7-dev libldap2-dev libsasl2-dev
```

RedHat/CentOS:
```
yum install python-devel openldap-devel
```

```
pip install python-ldap
```

Windows:

https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-ldap

python_ldap‑3.3.1‑cp36‑cp36m‑win_amd64.whl


## Win 2K3 安装 AD Server

连接CD/DVD驱动器, 选择 Win 2K3 镜像 (过程中安装DNS需要)

运行, dcpromo, 一路下一步

测试连接
```
In [1]: import ldap

In [2]: con = ldap.initialize('ldap://192.168.1.3:389', bytes_mode=False)

In [3]: con.simple_bind_s()
Out[3]: (97, [], 1, [])
```
