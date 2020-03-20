# Tcpdump

```
tcpdump -i any
tcpdump -i any -c 10 -nn
```

参数 | 描述
--- | ---
-i | 指定网络接口（any：全部）
-n | 选项显示 IP 地址
-nn | 选项显示端口号
host | 只抓取和特定主机相关的数据包
port | 只抓取和特定端口相关的数据包
src | 根据源 IP 地址或者主机名来筛选数据包
dst | 根据目的 IP 地址或者主机名来筛选数据包


多条件筛选:
and 以及 or
