# Plugin

[https://github.com/uken/fluent-plugin-elasticsearch](https://github.com/uken/fluent-plugin-elasticsearch)


ES重连策略
```
efk@localhost:~$ docker logs fluentd | grep retry_time
2020-03-05 11:03:44 +0000 [warn]: #0 failed to flush the buffer. retry_time=0 next_retry_seconds=2020-03-05 11:03:45 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 11:03:50 +0000 [warn]: #0 failed to flush the buffer. retry_time=1 next_retry_seconds=2020-03-05 11:03:51 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 11:03:56 +0000 [warn]: #0 failed to flush the buffer. retry_time=2 next_retry_seconds=2020-03-05 11:03:58 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 11:04:03 +0000 [warn]: #0 failed to flush the buffer. retry_time=3 next_retry_seconds=2020-03-05 11:04:07 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 11:04:12 +0000 [warn]: #0 failed to flush the buffer. retry_time=4 next_retry_seconds=2020-03-05 11:04:21 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 11:04:26 +0000 [warn]: #0 failed to flush the buffer. retry_time=5 next_retry_seconds=2020-03-05 11:04:43 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 11:04:48 +0000 [warn]: #0 failed to flush the buffer. retry_time=6 next_retry_seconds=2020-03-05 11:05:20 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 11:05:25 +0000 [warn]: #0 failed to flush the buffer. retry_time=7 next_retry_seconds=2020-03-05 11:06:21 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 11:06:26 +0000 [warn]: #0 failed to flush the buffer. retry_time=8 next_retry_seconds=2020-03-05 11:08:44 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 11:08:49 +0000 [warn]: #0 failed to flush the buffer. retry_time=9 next_retry_seconds=2020-03-05 11:13:10 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 11:13:15 +0000 [warn]: #0 failed to flush the buffer. retry_time=10 next_retry_seconds=2020-03-05 11:22:20 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 11:22:25 +0000 [warn]: #0 failed to flush the buffer. retry_time=11 next_retry_seconds=2020-03-05 11:40:36 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 11:40:41 +0000 [warn]: #0 failed to flush the buffer. retry_time=12 next_retry_seconds=2020-03-05 12:12:32 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 12:12:37 +0000 [warn]: #0 failed to flush the buffer. retry_time=13 next_retry_seconds=2020-03-05 13:17:30 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 13:17:35 +0000 [warn]: #0 failed to flush the buffer. retry_time=14 next_retry_seconds=2020-03-05 15:20:53 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 15:20:59 +0000 [warn]: #0 failed to flush the buffer. retry_time=15 next_retry_seconds=2020-03-05 19:56:00 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
2020-03-05 19:56:05 +0000 [warn]: #0 failed to flush the buffer. retry_time=16 next_retry_seconds=2020-03-06 05:06:25 +0000 chunk="5a0197d3263c2d100a37668ee7d53a50" error_class=Fluent::Plugin::ElasticsearchOutput::RecoverableRequestFailure error="could not push logs to Elasticsearch cluster ({:host=>\"elasticsearch\", :port=>9200, :scheme=>\"http\", :user=>\"elastic\", :password=>\"obfuscated\"}): connect_write timeout reached"
```

[https://github.com/uken/fluent-plugin-elasticsearch/issues/525#issuecomment-475502715](https://github.com/uken/fluent-plugin-elasticsearch/issues/525#issuecomment-475502715)
```
reconnect_on_error true
reload_on_failure true
reload_connections false
```

插件官方还有1个解释，ES分配的CPU资源不足: [https://github.com/uken/fluent-plugin-elasticsearch#cannot-push-logs-to-elasticsearch-with-connect_write-timeout-reached-why](https://github.com/uken/fluent-plugin-elasticsearch#cannot-push-logs-to-elasticsearch-with-connect_write-timeout-reached-why)
但从监控指标上看，不支持这种说法

分析:
1、并发高导致的ES写入失败
2、因组件最小化原则，加上初期设计没有考虑到瞬时并发量，没有引入队列进行日志缓冲
3、重试机制，使用的还是原先的连接，只能解决网络本身波动的问题，解决不了这种连接本身错误的问题

当前改进:
1、出错需要重新建立新的连接
2、并加大延迟写入间隔

思考:
1、模拟足够的场景进行性能测试（并发读取、并发写入）
2、网络波动是否会对数据收集产生影响，如果有影响，具体是什么影响
3、并发写入失败之后如何正确处置


```
sudo docker logs fluentd --tail 10
sudo docker rm -f fluentd
sudo sh docker_run.sh
```
