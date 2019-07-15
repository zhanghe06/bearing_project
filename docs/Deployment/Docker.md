# Docker

Get Docker CE for CentOS
```
# yum install -y yum-utils device-mapper-persistent-data lvm2
# yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
# yum install -y docker-ce
# systemctl start docker
# docker -v
# docker ps
```
参考: [https://docs.docker.com/install/linux/docker-ce/centos/](https://docs.docker.com/install/linux/docker-ce/centos/)

Get Docker CE for Ubuntu
```
# apt-get update
# apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
# apt-key fingerprint 0EBFCD88
# add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
# apt-get update
# apt-get install docker-ce docker-ce-cli containerd.io
# docker -v
# docker ps
```
参考: [https://docs.docker.com/install/linux/docker-ce/centos/](https://docs.docker.com/install/linux/docker-ce/centos/)


Docker 中国官方镜像加速 registry mirror [https://registry.docker-cn.com](https://registry.docker-cn.com)


## 错误调试

拉取镜像报错
```
docker: Error response from daemon: Get https://registry-1.docker.io/v2/: EOF.
```

通过dig找到可用ip
```
➜  ~ dig @114.114.114.114 registry-1.docker.io

; <<>> DiG 9.10.6 <<>> @114.114.114.114 registry-1.docker.io
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 26129
;; flags: qr rd ra; QUERY: 1, ANSWER: 8, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;registry-1.docker.io.		IN	A

;; ANSWER SECTION:
registry-1.docker.io.	35	IN	A	52.22.201.61
registry-1.docker.io.	35	IN	A	34.232.31.24
registry-1.docker.io.	35	IN	A	34.233.151.211
registry-1.docker.io.	35	IN	A	52.22.67.152
registry-1.docker.io.	35	IN	A	34.205.207.96
registry-1.docker.io.	35	IN	A	52.206.40.44
registry-1.docker.io.	35	IN	A	34.206.236.31
registry-1.docker.io.	35	IN	A	34.228.211.243

;; Query time: 10 msec
;; SERVER: 114.114.114.114#53(114.114.114.114)
;; WHEN: Wed Mar 13 13:40:36 CST 2019
;; MSG SIZE  rcvd: 177
```

向hosts添加可用域名解析（有时候这一步不需要）
```
echo '52.22.201.61 registry-1.docker.io' >> /etc/hosts
```
