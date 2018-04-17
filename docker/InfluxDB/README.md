InfluxDB

https://hub.docker.com/_/influxdb/

```
$ sudo docker pull influxdb:1.4.2
```


生成默认配置文件
```
$ docker run --rm influxdb:1.4.2 influxd config > conf/influxdb.conf
```

https://github.com/influxdata/influxdb

https://docs.influxdata.com/influxdb/v1.4/



InfluxDB 中的名词与传统数据库中的概念

InfluxDB 名词 | 传统数据库中的概念
--- | ---
database | 数据库
measurement | 数据库中的表
points | 表里面的一行数据
series | 表里面的数据记录

InfluxDB 特有的概念

Point 属性 | 传统数据库中的概念
--- | ---
time | 时间戳, 每个数据记录时间, 是数据库中的主索引(会自动生成)
fields | 数据, 各种记录值（没有索引的属性）也就是记录的值: 温度, 湿度
tags | 标签, 各种有索引的属性: 地区, 海拔
