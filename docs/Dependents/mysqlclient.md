# mysqlclient

```
pip install mysqlclient
```

## 系统依赖

### CenxOS
```
yum install -y gcc
yum install -y mysql-devel
yum install -y python-devel
```

### Ubuntu
```
# mysql 版本
sudo apt-get install -y libmysqld-dev
sudo apt-get install -y libmysqlclient-dev
sudo apt-get install -y python-dev
# mariadb 版本
sudo apt-get install -y libmariadbd-dev
sudo apt-get install -y libmariadbclient-dev
sudo apt-get install -y python-dev
```

### MacOS
```
brew unlink mariadb
brew install mariadb-connector-c
ln -s /usr/local/opt/mariadb-connector-c/bin/mariadb_config /usr/local/bin/mysql_config
```
