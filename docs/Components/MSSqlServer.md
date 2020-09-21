# MSSqlServer

## 系统: Win Server 2008 R2 X64

### 系统激活

windows server 2008/R2 KMS密钥激活步骤

1、点击开始图标打开开始菜单，在搜索框输入cmd，右键cmd，选择“以管理员身份运行”；
2、打开命令提示符，依次执行下面的代码
```
# 安装server2008密钥
slmgr /ipk 489J6-VHDMP-X63PK-3K798-CPX3Y
# 设置kms服务器
slmgr /skms zh.us.to
# 激活server2008
slmgr /ato
# 查询激活期限，kms一般是180天，到期后再次激活
slmgr /xpr
```

### 关闭防火墙

### 宿主机将文件传入虚拟机

```bash
python -m SimpleHTTPServer 8866
```

[http://0.0.0.0:8866](http://0.0.0.0:8866)


### 禁用 IE ESC

### 开启 .NET Framework
```
开始 >> 管理工具 >> 服务器管理器 >> 功能 >> 添加功能 >> 勾选 .NET Framework 3.5.1 >> 下一步 >> 安装
```

### 安装 VMware Tools，此步骤，依赖 `.NET Framework 3.5.1`

服务端

[Microsoft® SQL Server® 2008 R2 SP2 - Express Edition](https://www.microsoft.com/zh-CN/download/details.aspx?id=30438)

客户端

[Microsoft SQL Server 2008 R2 RTM - Management Studio Express](https://www.microsoft.com/zh-CN/download/details.aspx?id=22985)

```
账号: sa
密码: 1qazXSW@
```

初始化配置
```
# 开启 TCP/IP
Sql Server Configuration Manager >> SQL Server 网络配置
1. SQLEXPRESS 的协议 >> TCP/IP 右键属性 >> IPALL >> TCP动态端口清空，并设置TCP端口为1433
2. SQLEXPRESS 的协议 >> TCP/IP 右键启用

# 开启 SQL Server Brower
Sql Server Configuration Manager >> SQL Server 配置管理器 >> SQL Server 服务
1. SQL Server Brower 右键属性 >> 服务 >> 启动模式（自动） >> 应用
2. SQL Server Brower 右键启动
```

关闭防火墙

测试远程连接

DataGrip 配置（Mac 使用jtds驱动）

参考: [https://blog.jetbrains.com/datagrip/2016/06/21/connecting-datagrip-to-ms-sql-server](https://blog.jetbrains.com/datagrip/2016/06/21/connecting-datagrip-to-ms-sql-server)
```
jdbc:jtds:sqlserver://192.168.64.244:1433;instance=SQLEXPRESS
```

配置完General, 再从Schemas中选择对应的数据库

sqlalchemy 驱动

[http://docs.sqlalchemy.org/en/latest/dialects/mssql.html](http://docs.sqlalchemy.org/en/latest/dialects/mssql.html)

```
mssql+pymssql://<username>:<password>@<freetds_name>/?charset=utf8
```

Mac 安装 freetds(pymssql的依赖)

[http://pymssql.org/en/stable/freetds.html](http://pymssql.org/en/stable/freetds.html)

```
brew unlink freetds
brew install freetds@0.91
brew link --overwrite --force freetds@0.91
echo 'export PATH="/usr/local/opt/freetds@0.91/bin:$PATH"' >> ~/.zshrc
```

2020-08-31更新：

直接安装freetds即可，新版pymssql对freetds版本依赖的限制已经修复
```
brew install freetds
```

查看服务信息
```
✗ tsql -LH 192.168.64.149
     ServerName WIN-MJT54M4U9AM
   InstanceName SQLEXPRESS
    IsClustered No
        Version 10.50.4000.0
            tcp 49460
```

测试连接
```
✗ tsql -H 192.168.64.149 -U sa -P 1qazXSW@ -p 1433
locale is "C/UTF-8/C/C/C/C"
locale charset is "UTF-8"
using default charset "UTF-8"
1>
```

python 客户端 pymssql
```
pip install pymssql
```

测试连接

1. pymssql 客户端方式

```
import pymssql

conn = pymssql.connect('192.168.64.196\SQLEXPRESS', 'sa', '1qazXSW@', "UFTData018618_000666")
cursor = conn.cursor()
cursor.execute('SELECT * FROM AA_Partner')
row = cursor.fetchone()
while row:
    print("ID=%s, Name=%s" % (row[0], row[1]))
    row = cursor.fetchone()
conn.close()
```

2. sqlalchemy 方式

```
from sqlalchemy import create_engine

conn_str = 'mssql+pymssql://%s:%s@%s/UFTData018618_000666' % ('sa', '1qazXSW@', '192.168.64.196\SQLEXPRESS')
engine = create_engine(conn_str)
connection = engine.connect()
result = connection.execute("SELECT * FROM AA_Partner")
row = result.fetchone()
print("ID=%s, Name=%s" % (row[0], row[1]))
connection.close()
```
