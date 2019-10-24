## Nginx

https://hub.docker.com/_/nginx/
```
$ sudo docker pull nginx:1.13.0
```


The :ro option causes these directors to be read only inside the container.


证书创建过程：

```
sh create_ca.sh
sh create_csr.sh
sh create_key.sh
sh create_crt.sh
```

创建记录
```
➜  Nginx git:(master) ✗ sh create_ca.sh
Generating RSA private key, 1024 bit long modulus
.++++++
..................++++++
e is 65537 (0x10001)
Enter pass phrase for conf/ssl/ca.key:123456
Verifying - Enter pass phrase for conf/ssl/ca.key:123456
➜  Nginx git:(master) ✗ sh create_csr.sh
Enter pass phrase for conf/ssl/ca.key:123456
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) []:CN
State or Province Name (full name) []:Shang Hai
Locality Name (eg, city) []:Yang Pu
Organization Name (eg, company) []:Bearing
Organizational Unit Name (eg, section) []:Bearing Co., Ltd.
Common Name (eg, fully qualified host name) []:Bearing CA
Email Address []:zhendime@gmail.com

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
➜  Nginx git:(master) ✗ sh create_key.sh
Enter pass phrase for conf/ssl/ca.key:123456
writing RSA key
➜  Nginx git:(master) ✗ sh create_crt.sh
Signature ok
subject=/C=cn/ST=shanghai/L=yangpu/O=bearing/OU=python/CN=mac/emailAddress=abc@xyz.com
Getting Private key
```

如果启用https,如果需要强制跳转,需要取消其它配置文件
```
docker/nginx/conf/conf.d/default.conf >> docker/nginx/conf/conf.d/default.conf.bak
docker/nginx/conf/conf.d/project.conf >> docker/nginx/conf/conf.d/project.conf.bak
```

浏览器自签名证书配置

将 docker/Nginx/conf/ssl/server.crt 导入, 并设置始终信任

IE浏览器证书配置
```
Internet 选项 >> 内容 >> 证书 >> 受信任的根证书颁发机构 >> 导入 >> 下一步 >> 浏览 >> 选择 >> 弹出提示，选是 
```

Windows 修改 hosts `C:\Windows\System32\drivers\etc\hosts`


验证IP
```
curl http://192.168.4.1:8000/ip
curl -k https://192.168.4.1:8000/ip
curl -k https://www.app.com/ip
curl -k -H "X-Forwarded-For: 1.2.3.4" https://www.app.com/ip
```


## 参数解析

`proxy_next_upstream` 自动重试，默认`error timeout`
`proxy_next_upstream_tries` 设置重试次数，默认0表示不限制，注意此重试次数指的是所有请求次数（包括第一次和之后的重试次数之和）。
`proxy_next_upstream_timeout` 设置重试最大超时时间，默认0表示不限制。

参考：[http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_next_upstream](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_next_upstream)

```
normally, requests with a non-idempotent method (POST, LOCK, PATCH) are not passed to the next server if a request has been sent to an upstream server (1.9.13); enabling this option explicitly allows retrying such requests;
```

也就是说，一般情况下，幂等的操作会重试，而非幂等的操作不会重试。也可以`non_idempotent`参数使得非幂等操作一样重试

HTTP方法
- 非幂等：POST、LOCK、PATCH
- 幂等：GET、HEAD、PUT、DELETE、OPTIONS、TRACE


## 采坑

windows 下接口特别慢，部分接口出现响应1分钟，时间特别有规律，就是1分钟

proxy_pass localhost换成了127.0.0.1，速度飞起
