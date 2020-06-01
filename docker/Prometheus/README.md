## Prometheus

```
docker pull prom/prometheus:v2.16.0
```

[https://hub.docker.com/r/prom/prometheus](https://hub.docker.com/r/prom/prometheus)

[https://github.com/prometheus/prometheus](https://github.com/prometheus/prometheus)


管理页面
[http://localhost:9090](http://localhost:9090)

查看监控目标
[http://localhost:9090/targets](http://localhost:9090/targets)


### Doc

[https://prometheus.io/docs/introduction/overview](https://prometheus.io/docs/introduction/overview)

[https://prometheus.io/docs/prometheus/latest/querying/basics](https://prometheus.io/docs/prometheus/latest/querying/basics)


### Prometheus Basic Auth

Prometheus 的 Node Exporter 并没有提供任何认证支持。
不过，借助 Nginx 作为反向代理服务器，我们可以很容易地为 Node Exporter 添加 HTTP Basic Auth 功能。

```
$ htpasswd -c .htpasswd your-username
New password: 
Re-type new password: 
Adding password for user your-username
```

```
http {
  server {
    listen 0.0.0.0:19090;
    location / {
      proxy_pass http://localhost:9090/;

      auth_basic "Prometheus";
      auth_basic_user_file ".htpasswd";
    }
  }
}
```

```
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['your-ip:19090']
    basic_auth:
      username: your-username
      password: your-password
```

### 规模化部署

1. Prometheus本身不适用于持久化存储长期的历史数据，默认情况下Prometheus只保留15天的数据。
2. 本地存储也意味着Prometheus自身无法进行有效的弹性伸缩。

需要思考的问题:
1. 单点问题
2. 大量存储
3. 大量写入


### 高可用

[https://github.com/yunlzheng/prometheus-book/blob/master/ha/prometheus-and-high-availability.md](https://github.com/yunlzheng/prometheus-book/blob/master/ha/prometheus-and-high-availability.md)
