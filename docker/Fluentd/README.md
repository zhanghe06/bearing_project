## Fluentd

[https://hub.docker.com/_/fluentd](https://hub.docker.com/_/fluentd)

[Fluentd Docker Compose](https://docs.fluentd.org/container-deployment/docker-compose)

```
docker pull fluentd:v1.8
```

[https://github.com/uken/fluent-plugin-elasticsearch](https://github.com/uken/fluent-plugin-elasticsearch)

[https://rubygems.org/gems/fluent-plugin-elasticsearch](https://rubygems.org/gems/fluent-plugin-elasticsearch)

### Plugins
Fluentd has 8 types of plugins: 
Input, Parser, Filter, Output, Formatter, Storage, Service Discovery and Buffer. 


#### Input

[https://docs.fluentd.org/input](https://docs.fluentd.org/input)

输入源可以一次指定多个， @type参数指定使用哪一个输入插件。
fluentd支持各种输入插件, 比如:

in_tail
in_forward
in_udp
in_tcp
in_unix
in_http
in_syslog
in_exec
in_dummy
in_windows_eventlog


#### Parser

[https://docs.fluentd.org/parser](https://docs.fluentd.org/parser)

神器: [a Fluentd regular expression editor](http://fluentular.herokuapp.com)


#### Filter

[https://docs.fluentd.org/filter](https://docs.fluentd.org/filter)


#### Output

[https://docs.fluentd.org/output](https://docs.fluentd.org/output)

out_copy
out_null
out_roundrobin
out_stdout
out_exec_filter
out_forward
out_mongo or out_mongo_replset
out_exec
out_file
out_s3
out_webhdfs


#### Data Types

https://docs.fluentd.org/configuration/config-file#supported-data-types-for-values

retry_wait 默认值为1.0秒，未设置（无限制）。间隔加倍（+/- 12.5％随机性），每次重试，直到达到max_retry_wait
max_retry_wait 在默认配置中，最后一次重试等待大约131072秒，大约36小时

retry_limit
disable_retry_limit


### 配置详解

[https://blog.gmem.cc/efk-as-a-log-analysis-system](https://blog.gmem.cc/efk-as-a-log-analysis-system)
