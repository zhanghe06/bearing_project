## Elasticsearch

[https://hub.docker.com/_/elasticsearch](https://hub.docker.com/_/elasticsearch)

[https://www.docker.elastic.co](https://www.docker.elastic.co)

重要: [https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)

```
$ docker pull elasticsearch:7.6.0
```

```
$ curl --basic -u elastic:changeme http://127.0.0.1:9200/_cat/health
1523173079 07:37:59 docker-cluster green 1 1 1 1 0 0 0 0 - 100.0%
```

注意：如果是特殊密码需要转义
```
username: elastic
password: $sHz!7cnJ5
# 速记：啥时候这疫情才能结束
```

```
curl --basic -u elastic:\$sHz\!7cnJ5 http://127.0.0.1:9200/_cat/health
```
注意，特殊符号需要转义（$和!）


单点单节点部署Elasticsearch, 集群状态可能为yellow

因为单点部署Elasticsearch, 默认的分片副本数目配置为1，而相同的分片不能在一个节点上，所以就存在副本分片指定不明确的问题，所以显示为yellow，可以通过在Elasticsearch集群上添加一个节点来解决问题，如果不想这么做，可以删除那些指定不明确的副本分片（当然这不是一个好办法）但是作为测试和解决办法还是可以尝试的

Built-in Users
```
elastic
A built-in superuser. See Built-in Roles.
kibana
The user Kibana uses to connect and communicate with Elasticsearch.
logstash_system
The user Logstash uses when storing monitoring information in Elasticsearch.
```

### 插件

#### Elasticsearch-Head（web管理）

A web front end for an Elasticsearch cluster

[Elasticsearch-Head Chrome extension](https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm)

打开扩展进入页面，地址填入[http://localhost:9200/](http://localhost:9200/)，连接，界面显示集群状态


#### IK（中文分词）

分词测试

ik_smart 粗粒度
```bash
curl -XGET "http://localhost:9200/catalogue/_analyze?pretty=true" -H 'Content-Type: application/json' -d'
{
   "text":"7008CEGA/P4A","tokenizer": "ik_smart"
}'
```

```
{
  "tokens" : [
    {
      "token" : "7008cega",
      "start_offset" : 0,
      "end_offset" : 8,
      "type" : "LETTER",
      "position" : 0
    },
    {
      "token" : "p4a",
      "start_offset" : 9,
      "end_offset" : 12,
      "type" : "LETTER",
      "position" : 1
    }
  ]
}
```

ik_max_word 细粒度
```bash
curl -XGET "http://localhost:9200/catalogue/_analyze?pretty=true" -H 'Content-Type: application/json' -d'
{
   "text":"7008CEGA/P4A","tokenizer": "ik_max_word"
}'
```
```
{
  "tokens" : [
    {
      "token" : "7008cega",
      "start_offset" : 0,
      "end_offset" : 8,
      "type" : "LETTER",
      "position" : 0
    },
    {
      "token" : "7008",
      "start_offset" : 0,
      "end_offset" : 4,
      "type" : "ARABIC",
      "position" : 1
    },
    {
      "token" : "cega",
      "start_offset" : 4,
      "end_offset" : 8,
      "type" : "ENGLISH",
      "position" : 2
    },
    {
      "token" : "p4a",
      "start_offset" : 9,
      "end_offset" : 12,
      "type" : "LETTER",
      "position" : 3
    },
    {
      "token" : "p",
      "start_offset" : 9,
      "end_offset" : 10,
      "type" : "ENGLISH",
      "position" : 4
    },
    {
      "token" : "a",
      "start_offset" : 11,
      "end_offset" : 12,
      "type" : "ENGLISH",
      "position" : 5
    }
  ]
}
```

kibana 分析
```
GET /catalogue/_search
{
  "query": {
    "match": {
      "product_label": "7008 ACD GA / P4A"
    }
  },
  "highlight": {
    "pre_tags": [
      """<span class="text-primary">"""
    ],
    "post_tags": [
      "</span>"
    ],
    "fields": {
      "product_label": {}
    }
  }
}
```


内存分配

1. 不要超过内存总量的一半
2. 不要超过32GB

参考: https://www.elastic.co/guide/en/elasticsearch/guide/current/heap-sizing.html#compressed_oops

[https://www.elastic.co/guide/cn/elasticsearch/guide/current/_limiting_memory_usage.html#fielddata-size](https://www.elastic.co/guide/cn/elasticsearch/guide/current/_limiting_memory_usage.html#fielddata-size)

[https://www.elastic.co/guide/cn/elasticsearch/guide/current/heap-sizing.html](https://www.elastic.co/guide/cn/elasticsearch/guide/current/heap-sizing.html)

[https://www.elastic.co/guide/cn/elasticsearch/guide/current/aggregations-and-analysis.html](https://www.elastic.co/guide/cn/elasticsearch/guide/current/aggregations-and-analysis.html)

[https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-fielddata.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-fielddata.html)

堆内存分配

ES_JAVA_OPTS设置为分配内存的一半


### 排错

```
{"type": "server", "timestamp": "2020-04-15T16:18:07,770Z", "level": "WARN", "component": "o.e.b.BootstrapChecks", "cluster.name": "docker-cluster", "node.name": "elasticsearch", "message": "max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]" }
```


### 生产环境优化

[https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-prod-prerequisites](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-prod-prerequisites)

[https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html)

- vm.max_map_count
`/etc/sysctl.conf`

或者`/proc/sys/vm/max_map_count`

Linux
```
# grep vm.max_map_count /etc/sysctl.conf
# sysctl -w vm.max_map_count=262144
# grep vm.max_map_count /etc/sysctl.conf
vm.max_map_count=262144
```

macOS with Docker for Mac
```
➜  ~ screen ~/Library/Containers/com.docker.docker/Data/vms/0/tty
➜  ~ sysctl -w vm.max_map_count=262144
```

- nofile
`/etc/security/limits.conf`

```
$ sudo su
# ulimit -n 65535
# su elasticsearch
$ ulimit -a
```

```
* soft nofile 65535
* hard nofile 65535
```

```
# echo "* hard nofile 65535
* soft nofile 65535
root hard nofile 65535
root soft nofile 65535" >> /etc/security/limits.conf
# reboot
```

检查max_file_descriptors
[http://localhost:5601](http://localhost:5601)
```
GET _nodes/stats/process?filter_path=**.max_file_descriptors
```

```
{
  "nodes" : {
    "Q5hwQcJERZqZDtma4QHZkQ" : {
      "process" : {
        "max_file_descriptors" : 65536
      }
    }
  }
}
```

- nproc
`/etc/security/limits.conf`

```
# ulimit -u 4096
```

### 优化配置

/etc/security/limits.conf
```
root soft nofile 65536
root hard nofile 65536
* soft nofile 65536
* hard nofile 65536
```

/etc/sysctl.conf
```
net.core.somaxconn = 1024
net.core.netdev_max_backlog = 5000
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216relabel
net.ipv4.tcp_wmem = 4096 12582912 16777216
net.ipv4.tcp_rmem = 4096 12582912 16777216
net.ipv4.tcp_max_syn_backlog = 8096
net.ipv4.tcp_slow_start_after_idle = 0
net.ipv4.tcp_tw_reuse = 1
```
