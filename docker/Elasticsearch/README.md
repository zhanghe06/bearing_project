## Elasticsearch

https://www.docker.elastic.co

```
$ docker pull docker.elastic.co/elasticsearch/elasticsearch:6.2.3
```

```
$ curl http://127.0.0.1:9200/_cat/health
1523173079 07:37:59 docker-cluster green 1 1 1 1 0 0 0 0 - 100.0%
```

Built-in Users
```
elastic
A built-in superuser. See Built-in Roles.
kibana
The user Kibana uses to connect and communicate with Elasticsearch.
logstash_system
The user Logstash uses when storing monitoring information in Elasticsearch.
```


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