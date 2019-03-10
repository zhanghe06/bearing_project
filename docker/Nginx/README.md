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


验证IP
```
curl http://192.168.4.1:8000/ip
curl -k https://192.168.4.1:8000/ip
curl -k https://www.app.com/ip
curl -k -H "X-Forwarded-For: 1.2.3.4" https://www.app.com/ip
```
