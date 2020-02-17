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

