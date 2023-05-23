## Docker

Docker的监控原则：
根据docker官方声明，一个容器不建议跑多个进程，所以不建议在容器中使用agent进行监控（zabbix等），agent应该运行在宿主机，通过cgroup或是docker api获取监控数据。

容器操作，涉及数据变化的持久化，需要用`link`，否则直接`docker exec`


### Docker Hub
```
docker login -u 用户名 -p 密码
```

### docker save

[https://docs.docker.com/engine/reference/commandline/save](https://docs.docker.com/engine/reference/commandline/save)

```
docker save -o fedora-latest.tar fedora:latest
docker save myimage:latest | gzip > myimage_latest.tar.gz

docker load -i fedora-latest.tar
docker load -i myimage_latest.tar.gz
```

### docker删除名称none镜像
```bash
docker rmi $(docker images -f "dangling=true" -q)
```

### 显示非k8s容器
```bash
docker ps | grep -v k8s
```

### docker 配置

MacOS docker 代理配置（平时注意关闭）
```
Settings -> Resources -> PROXIES -> Manual proxy configuration
```

https://docs.docker.com/engine/reference/commandline/dockerd/

```
{
    "registry-mirrors": [ "https://registry.docker-cn.com"],
    "insecure-registries": [ "172.18.18.90:5000"]
}
```

[阿里云Docker官方镜像](https://cr.console.aliyun.com/cn-hangzhou/instances/mirrors)
使用加速器可以提升获取Docker官方镜像的速度

- registry-mirrors 拉取加速
- insecure-registries 上推认证


### 查看 docker 状态和指标

```
docker ps -a --format {{.Names}}
docker inspect --format="{{.State.Running}}" redis
docker inspect --format="{{.HostConfig.RestartPolicy.Name}}" redis
docker stats redis --no-stream --format "{{.CPUPerc}}"
docker stats --format "table{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
docker stats redis --no-stream --format "table{{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

docker stats --no-stream
docker ps --format "table{{.Names}}\t{{.Status}}"

# 查看日志驱动
docker info --format '{{.LoggingDriver}}'

# 查看存储目录
docker info | grep "Docker Root Dir"
```

format name | description
--- | ---
.Container | 根据用户指定的名称显示容器的名称或ID
.Name | 容器名称
.ID | 容器 ID
.CPUPerc | CPU 使用率
.MemUsage | 内存使用量
.NetIO | 网络 I/O
.BlockIO | 磁盘 I/O
.MemPerc | 内存使用率
.PIDs | PID 号


### 批量删除镜像

```bash
docker images | grep <镜像的关键字> | awk '{print "docker rmi "$3}' | sh
docker images | grep <镜像的关键字> | awk '{print "docker rmi "$1":"$2}' | sh
```
`$2`可能为None，删除会报错
`$3`为镜像ID，如果遇到同一ID打了多个标签，仅仅通过ID删除会报错

### 批量删除容器
```bash
docker ps --format {{.Names}} | grep <容器的关键字> | awk '{print "docker rm -f "$1}' | sh
```

### 资源限制

[https://docs.docker.com/config/containers/resource_constraints](https://docs.docker.com/config/containers/resource_constraints)

查看帮助
```
# docker help run
  -m, --memory bytes                   Memory limit
      --memory-swap bytes              Swap limit equal to memory plus swap: '-1' to enable unlimited swap
  -c, --cpu-shares int                 CPU shares (relative weight)
      --cpus decimal                   Number of CPUs
```

1、限制内存（--memory 和 --memory-swap设置一样表示不使用交换空间）
```
-m="1g" --memory-swap="1g"
```

2、限制CPU（--cpu-shares 共享配额，--cpus限制最大核心数量）
```
--cpus 2
```

### 大文件查看

```
head -n 10 /etc/profile  # 前10行
tail -n 10 /etc/profile  # 后10行
```

### 查看端口占用

```
netstat -ant | awk '{print $4}' | grep -E ":9200|:9300|:24224|:5601"
```

### 指定用户

```
--user $(id -u)
```

### 数据卷

```
docker volume create grafana-vol
docker volume ls | grep grafana
docker volume inspect grafana-vol

docker volume rm grafana-vol
docker volume prune
```

数据卷迁移
```
docker inspect mongo

```


### 指定储存目录

```
cat << EOF >>/etc/docker/daemon.json
{
    "data-root": "/mnt/docker-data"
}
EOF

systemctl restart docker 
```

### 修改容器配置
```
$ sudo docker container update --restart=always fluentd
fluentd
$ sudo docker inspect --format="{{.HostConfig.RestartPolicy.Name}}" fluentd
always
```

### 控制日志大小


```
# 查看所有容器日志大小
sudo du -sh /var/lib/docker/containers/
# 查看指定容器日志大小
docker inspect --format {{.LogPath}} fluentd | xargs sudo du -sh
# 查看日志目录大小
du -BG -d 2
```


控制容器日志大小
```
docker run \
    --log-opt max-size=10m \
    --log-opt max-file=3 \
    ...
```

[https://docs.docker.com/config/containers/logging/json-file](https://docs.docker.com/config/containers/logging/json-file)


Ubuntu版本	| debian版本号	| debian代号
---------   | -----------   | ---------
14.04	    | 8	            | jessie
16.04	    | 9	            | strech
18.04	    | -	            | buster
