## Grafana

[https://hub.docker.com/r/grafana/grafana](https://hub.docker.com/r/grafana/grafana)

[https://github.com/grafana/grafana](https://github.com/grafana/grafana)

```
docker pull grafana/grafana:6.6.2
```

[http://localhost:3000](http://localhost:3000)

默认账号密码：admin/admin

首次登陆，提示更新密码，也可跳过

1. Configuration -> Data Sources 添加数据源（选择Prometheus, http://192.168.4.1:9090）
2. Create Import, Dashboard 填入[11074](https://grafana.com/grafana/dashboards/11074), 数据源选择刚添加的Prometheus

容器的模板：
[893](https://grafana.com/grafana/dashboards/893)
[193](https://grafana.com/grafana/dashboards/193)
[11277](https://grafana.com/grafana/dashboards/11277)


常用变量设置

Name | Label | Query | Regex
--- | --- | --- | ---
job | Job | label_values(node_uname_info, job) | -
hostname | Host | label_values(node_uname_info{job=~"$job"}, nodename) | -
instance | Instance | label_values(container_cpu_user_seconds_total{job=~"$job"}, instance) | -


Grafana社区用户分享的Dashboard: [https://grafana.com/dashboards](https://grafana.com/dashboards)


### 创建用户

```
# 1、创建用户
Server Admin -> Users -> New user -> 填入: Name、Username、Password

# 2、配置权限
Configuration -> Users -> Role -> Viewer
```


### Using Elasticsearch in Grafana

[https://grafana.com/docs/grafana/latest/features/datasources/elasticsearch](https://grafana.com/docs/grafana/latest/features/datasources/elasticsearch)

[Elasticsearch Templated Dashboard](https://play.grafana.org/dashboard/db/elasticsearch-templated)


### Alerting

Template variables are not supported in alert queries

变量条件查询不支持告警

变通方式: 提供隐藏的确定条件查询
