## MySQL Server Exporter

https://hub.docker.com/r/prom/mysqld-exporter/

https://github.com/prometheus/mysqld_exporter

配置用户及权限
```
➜  MySQLServerExporter git:(master) ✗ sh create_user.sh
+-----------+----------+
| host      | user     |
+-----------+----------+
| %         | root     |
| %         | www      |
| localhost | exporter |
| localhost | root     |
+-----------+----------+
```

启动服务(需提前启动MariaDB容器)
```bash
sh docker_run.sh
```

[http://localhost:9104/metrics](http://localhost:9104/metrics)


创建允许远程访问用户示例
```
sh -c 'exec mysql \
    -h"$MYSQL_PORT_3306_TCP_ADDR" \
    -P"$MYSQL_PORT_3306_TCP_PORT" \
    -uroot \
    -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD" \
    --default-character-set=utf8 \
    "$MYSQL_ENV_MYSQL_DATABASE" \
    -e "CREATE USER 'exporter'@'\'%\'' IDENTIFIED BY '\'123456\'';"'
```
