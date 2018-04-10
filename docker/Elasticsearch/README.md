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
