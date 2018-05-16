## Docker

Get Docker CE for CentOS
```
# yum install -y yum-utils device-mapper-persistent-data lvm2
# yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
# yum install -y docker-ce
# systemctl start docker
# docker -v
# docker ps
```
参考: https://docs.docker.com/install/linux/docker-ce/centos/
