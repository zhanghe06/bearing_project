# Docker

Docker的监控原则：
根据docker官方声明，一个容器不建议跑多个进程，所以不建议在容器中使用agent进行监控（zabbix等），agent应该运行在宿主机，通过cgroup或是docker api获取监控数据。

容器操作，涉及数据变化的持久化，需要用`link`，否则直接`docker exec`



## docker删除名称none镜像
```bash
docker rmi $(docker images -f "dangling=true" -q)
```

## 显示非k8s容器
```bash
docker ps | grep -v k8s
```
