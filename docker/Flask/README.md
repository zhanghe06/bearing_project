# Flask

python 3.6 镜像
```
docker pull python:3.6-alpine
```

调试
```
docker run -it python:3.6-alpine sh
```

Dockerfile
```
FROM python:3.6-alpine

RUN set -eux && sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk add --no-cache -U build-base openldap-dev mysql-dev linux-headers && \
    rm -rf /var/cache/apk/* && \
    pip install --no-cache-dir python-ldap requests mysqlclient uWSGI
```

镜像构建
```
docker build \
        --rm=true \
        --pull \
        -t flask \
        -f Dockerfile .
docker save -o flask-latest.tar flask:latest
```

```
docker build --rm=true --pull -t harbor.yovole.tech/ipam/python36:alpine -f Dockerfile .
docker save -o python36:alpine.tar harbor.yovole.tech/ipam/python36:alpine
```

pip 源配置
```
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
```
