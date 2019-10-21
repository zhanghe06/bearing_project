# 主备（Master Slave）

主备模式

9.5 版本以前，只能重新追随新主做一次全新的基础备份(pg_basebackup)，如果数据库较大，停机时间较长。
后续版本，支持倒带(pg_rewind)

### 环境变量（2个节点）

/etc/profile
```
[root@node1 ~] cat > /etc/profile << EOT
export PGHOME=/usr/pgsql-10
export PGDATA=/var/lib/pgsql/10/data
export LD_LIBRARY_PATH=$PGHOME/lib:$LD_LIBRARY_PATH
export PATH=$PGHOME/bin:$PATH
EOT
[root@node1 ~] source /etc/profile
```

### 密码配置（2个节点）

```
[root@node1 ~]# pg_md5 123456
e10adc3949ba59abbe56e057f20f883e
[root@node1 ~]# su - postgres
-bash-4.2$ pwd
/var/lib/pgsql
-bash-4.2$ cat > $HOME/.pgpass << EOT
node1:5432:replication:replica:123456
node2:5432:replication:replica:123456
EOT
-bash-4.2$ chmod 0600 $HOME/.pgpass
-bash-4.2$ chown postgres:postgres $HOME/.pgpass
```

### 配置文件
/var/lib/pgsql/10/data/postgresql.conf
```
wal_log_hints = on  # 默认off，pg_rewind需要开启，不然会报错：目标服务器需要使用数据校验和或者让"wal_log_hints = on"
```

注意：
- wal_level 在9.6之前的版本中，该参数还允许使用archive和hot_standby值。这些仍然被接受，但映射到replica。

### 恢复配置文件
/var/lib/pgsql/10/data/recovery.conf

配置文件 | 命令 | 备注
--- | --- | ---
postgresql.conf | archive_command = 'cp %p /var/lib/pgsql/archivedir/%f' | 归档
recovery.conf | restore_command = 'scp node1:/var/lib/pgsql/archivedir/%f %p' | 恢复数据


### 配置扩展，支持恢复功能

node1
```
[root@node1 ~]# su - postgres
-bash-4.2$ psql
postgres=# CREATE EXTENSION pgpool_recovery;
```

node2
```
[root@node2 ~]# su - postgres
-bash-4.2$ psql template1
template1=# CREATE EXTENSION pgpool_recovery;
```

## 主备切换（Failover）

### 一、关闭主库（模拟故障）
```
[root@node1 ~]# systemctl stop postgresql-10
```

### 二、激活原备提升为主
```
[root@node2 ~]# su - postgres
-bash-4.2$ /usr/pgsql-10/bin/pg_ctl promote
-bash-4.2$ psql -c "select pg_switch_wal();"
```

可以看到2个变化：
XXXXXX 1. /var/lib/pgsql/10/data/postgresql.conf 配置`hot_standby = on`已更新为`#hot_standby = off`
2. /var/lib/pgsql/10/data/recovery.conf 变为 /var/lib/pgsql/10/data/recovery.done


注意：10以前的版本是：pg_switch_xlog()

### 三、修复原主降级为备

**方案一:** 同步时间线，速度快，推荐（不成功）

同步时间线
```
[root@node1 ~]# systemctl stop postgresql-10  # 目标服务器必须被干净地关闭，确保原主服务关闭
[root@node1 ~]# su - postgres
-bash-4.2$ /usr/pgsql-10/bin/pg_rewind --target-pgdata $PGDATA --source-server='host=node2 port=5432 user=postgres dbname=postgres password=123456' -P
```

执行倒带（rewind）结果
```
已连接服务器
servers diverged at WAL location 0/17000098 on timeline 1
从时间线1上0/17000028处的最后一个普通检查点倒带
读取源文件列表
读取目标文件列表
读取目标中的WAL
需要复制 148 MB（整个源目录的大小是 167 MB）
已复制151898/151898 kB (100%)
正在创建备份标签并且更新控制文件
正在同步目标数据目录
完成！
```
或
```
已连接服务器
servers diverged at WAL location 0/1E000098 on timeline 2
不需要倒带（rewind）
```

如果原主时间线没有领先新主，pg_rewind会提示：不需要倒带（rewind）

cp /var/lib/pgsql/archivedir/* $PGDATA/pg_wal


可以发现:
1. 如果执行rewind，新备配置文件 /var/lib/pgsql/10/data/postgresql.conf 配置已经改为备库模式 hot_standby = on，如果提示不需要倒带，这里不变
2. 数据目录已复制新主节点的recovery.done(/var/lib/pgsql/10/data/recovery.done)，或者 没有生成

```
[root@node1 ~]# cat /var/lib/pgsql/10/data/recovery.done
standby_mode = 'on'
primary_conninfo = 'user=replica password=123456 host=node1 port=5432 sslmode=prefer sslcompression=1 krbsrvname=postgres target_session_attrs=any'
```

需要修改节点，并重命名为 recovery.conf
```
[root@node1 ~]# sed -i "s/node1/node2/g" /var/lib/pgsql/10/data/recovery.done                   # 修改配置
[root@node1 ~]# rm -f /var/lib/pgsql/10/data/recovery.conf                                      # 确保没有干扰文件
[root@node1 ~]# mv /var/lib/pgsql/10/data/recovery.done /var/lib/pgsql/10/data/recovery.conf    # 重命名
```

如果没有生成

```
[root@node1 ~]# sed -i "s/#hot_standby = off/hot_standby = on/g" /var/lib/pgsql/10/data/postgresql.conf
[root@node1 ~]# rm -f /var/lib/pgsql/10/data/recovery.done
[root@node1 ~]# cat > /var/lib/pgsql/10/data/recovery.conf << EOT
standby_mode = 'on'
primary_conninfo = 'user=replica password=123456 host=node2 port=5432 sslmode=prefer sslcompression=1 krbsrvname=postgres target_session_attrs=any'
EOT
[root@node1 ~]# chown postgres:postgres /var/lib/pgsql/10/data/recovery.conf
```

ls /var/lib/pgsql/10/data/pg_wal/
/var/lib/pgsql/archivedir/

**方案二:** 清库全新拉取新数据，速度慢，不推荐（成功）

```
[root@node1 ~]# systemctl stop postgresql-10
[root@node1 ~]# rm -rf ${PGDATA}
[root@node1 ~]# pg_basebackup -h node2 -U replica -Fp -Xs -v -P -R -D ${PGDATA}
[root@node1 ~]# chown postgres:postgres -R ${PGDATA}
[root@node1 ~]# sed -i "s/#hot_standby = off/hot_standby = on/g" /var/lib/pgsql/10/data/postgresql.conf
```

/var/lib/pgsql/10/data/recovery.conf 已通过`pg_basebackup`的`-R`参数自动生成


重启服务
```
[root@node1 ~]# systemctl restart postgresql-10
```

### 四、修改新主配置（貌似不需要）
```
[root@node2 ~]# sed -i "s/hot_standby = on/#hot_standby = off/g" /var/lib/pgsql/10/data/postgresql.conf
[root@node2 ~]# systemctl restart postgresql-10
```

### 五、校验主从
新主
```
[root@node2 postgresql]# ps -ef | grep wal
postgres  83024  83018  0 12:09 ?        00:00:00 postgres: wal writer process
postgres  83030  83018  0 12:09 ?        00:00:00 postgres: wal sender process replica 192.168.64.133(57250) streaming 0/21000328
```

新从
```
[root@node1 postgresql]# ps -ef | grep wal
postgres  59660  59610  0 12:09 ?        00:00:00 postgres: wal receiver process   streaming 0/21000328
```
