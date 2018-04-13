Nginx
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

如果启用https,如果需要强制跳转,需要取消其它配置文件
```
docker/nginx/conf/conf.d/default.conf >> docker/nginx/conf/conf.d/default.conf.bak
docker/nginx/conf/conf.d/project.conf >> docker/nginx/conf/conf.d/project.conf.bak
```


验证IP
```
curl http://192.168.4.1:8000/ip
curl -k https://192.168.4.1:8000/ip
curl -k https://www.app.com/ip
curl -k -H "X-Forwarded-For: 1.2.3.4" https://www.app.com/ip
```
