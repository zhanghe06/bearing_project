## Elasticsearch

[https://hub.docker.com/_/elasticsearch](https://hub.docker.com/_/elasticsearch)

[https://www.docker.elastic.co](https://www.docker.elastic.co)

```
$ docker pull elasticsearch:7.6.0
```

```
$ curl --basic -u "elastic:changeme" http://127.0.0.1:9200/_cat/health
1523173079 07:37:59 docker-cluster green 1 1 1 1 0 0 0 0 - 100.0%
```

注意：如果是特殊密码需要转义
```
username: elastic
password: $sHz!7cnJ5
# 速记：啥时候这疫情才能结束
```

```
curl --basic -u elastic:\$sHz\!7cnJ5 http://147.139.132.179:9200/_cat/health
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
}```


内存分配

不要超过内存总量的一半
不要超过32GB

参考: https://www.elastic.co/guide/en/elasticsearch/guide/current/heap-sizing.html#compressed_oops
