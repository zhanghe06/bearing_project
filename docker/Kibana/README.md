## Kibana

[https://hub.docker.com/_/kibana](https://hub.docker.com/_/kibana)

[https://www.docker.elastic.co](https://www.docker.elastic.co)

[kibana docker config](https://www.elastic.co/guide/en/kibana/current/docker.html#bind-mount-config)

```
docker pull kibana:7.6.0
```

[http://localhost:5601](http://localhost:5601)


Docker defaults
```
elasticsearch.username
elastic

elasticsearch.password
changeme
```

配置

Create index pattern（创建索引规则）

Step 1 of 2: Define index pattern
```
Management -> Kibana -> Index patterns -> fluentd-*
```

Step 2 of 2: Configure settings
```
I don't want to use the Time Filter
```

然后访问 Discover tab页

 
调试

kibana连不上es
```
# 1、先检查es是否通
curl --basic -u elastic:\$sHz\!7cnJ5 http://127.0.0.1:9200/_cat/health
# 2、再检查kibana
curl -i 127.0.0.1:5601
# 报503
# 3、检查kibana和es是否在一个网络组
```

### 查询

[https://www.elastic.co/guide/en/kibana/7.6/kuery-query.html](https://www.elastic.co/guide/en/kibana/7.6/kuery-query.html)
