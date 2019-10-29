# Nginx

## 限速
http://nginx.org/en/docs/http/ngx_http_limit_req_module.html

```nginx
http {
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;
    server {
        #限制每ip每秒不超过20个请求，漏桶数burst为5
        #brust的意思就是，如果第1秒、2,3,4秒请求为19个，
        #第5秒的请求为25个是被允许的。
        #但是如果你第1秒就25个请求，第2秒超过20的请求返回503错误。
        #nodelay，如果不设置该选项，严格使用平均速率限制请求数，
        #第1秒25个请求时，5个请求放到第2秒执行，
        #设置nodelay，25个请求将在第1秒执行。
        limit_req   zone=one  burst=1 nodelay;
    }
}
```

$binary_remote_addr 表示：客户端IP地址
zone 表示漏桶的名字
rate 表示nginx处理请求的速度有多快
burst 表示峰值
nodelay 表示是否延迟处理请求，还是直接503返回给客户端，如果超出rate设置的情况下。


## 反向代理域名
https://www.nginx.com/resources/wiki/modules/domain_resolve/

```nginx
http {
    resolver 8.8.8.8;
    resolver_timeout 10s;

    upstream backend {
        jdomain  www.baidu.com;
        # keepalive 10;
    }
    server {
        listen 8080;

        location / {
            proxy_pass http://backend;
        }
    }
}
```

注意windows环境下，proxy_pass指向localhost访问时非常慢，需要替换为127.0.0.1

```
# Localhost (DO NOT REMOVE)
127.0.0.1       localhost
```


## 日志切割
