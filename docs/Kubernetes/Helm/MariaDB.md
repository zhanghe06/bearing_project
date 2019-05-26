# MariaDB

```bash
helm install stable/mariadb --name my-mariadb
```

```
NOTES:

Please be patient while the chart is being deployed

Tip:

  Watch the deployment status using the command: kubectl get pods -w --namespace default -l release=my-mariadb

Services:

  echo Master: my-mariadb.default.svc.cluster.local:3306
  echo Slave:  my-mariadb-slave.default.svc.cluster.local:3306

Administrator credentials:

  Username: root
  Password : $(kubectl get secret --namespace default my-mariadb -o jsonpath="{.data.mariadb-root-password}" | base64 --decode)

To connect to your database:

  1. Run a pod that you can use as a client:

      kubectl run my-mariadb-client --rm --tty -i --restart='Never' --image  docker.io/bitnami/mariadb:10.1.38 --namespace default --command -- bash

  2. To connect to master service (read/write):

      mysql -h my-mariadb.default.svc.cluster.local -uroot -p my_database

  3. To connect to slave service (read-only):

      mysql -h my-mariadb-slave.default.svc.cluster.local -uroot -p my_database

To upgrade this helm chart:

  1. Obtain the password as described on the 'Administrator credentials' section and set the 'rootUser.password' parameter as shown below:

      ROOT_PASSWORD=$(kubectl get secret --namespace default my-mariadb -o jsonpath="{.data.mariadb-root-password}" | base64 --decode)
      helm upgrade my-mariadb stable/mariadb --set rootUser.password=$ROOT_PASSWORD
```

开启外部访问
```bash
kubectl port-forward --namespace default svc/my-mariadb 3366:3306 &
```

## 说明

主备复制架构，其中备库不对用户开放，不允许用户直接访问


## 默认配置
```
[mysqld]
skip-name-resolve
explicit_defaults_for_timestamp
basedir=/opt/bitnami/mariadb
port=3306
socket=/opt/bitnami/mariadb/tmp/mysql.sock
tmpdir=/opt/bitnami/mariadb/tmp
max_allowed_packet=16M
bind-address=0.0.0.0
pid-file=/opt/bitnami/mariadb/tmp/mysqld.pid
log-error=/opt/bitnami/mariadb/logs/mysqld.log
character-set-server=UTF8
collation-server=utf8_general_ci

[client]
port=3306
socket=/opt/bitnami/mariadb/tmp/mysql.sock
default-character-set=UTF8

[manager]
port=3306
socket=/opt/bitnami/mariadb/tmp/mysql.sock
pid-file=/opt/bitnami/mariadb/tmp/mysqld.pid
```

## 扩展配置
```
slow_querry_log=on              # 慢查询

log_bin=/log/mysql/mysql-bin    # 二进制日志
binlog_format=mixed             # 二进制日志记录的格式
max_binlog_size=1073741824      # 单个二进制日志文件的最大体积，默认1G
sync_binlog=1|0                 # 设定是否启动二进制日志同步功能，1是实时写入（遇到commit时）
```

## RDS 功能

1、模板列表、模板详情、模板创建、模板删除
2、实例列表、实例详情、实例创建、实例删除
