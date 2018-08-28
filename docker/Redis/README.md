Redis
https://hub.docker.com/_/redis/
```
$ sudo docker pull redis:3.2.8
```

--protected-mode no

设置密码

服务端启动
```
# sh docker/redis/docker_run_rdb_with_password.sh
```

客户端连接（普通方式）
```
# sh cli.sh
redis:6379> INFO Clients
(error) NOAUTH Authentication required.
redis:6379> AUTH 123456
OK
redis:6379> INFO Clients
# Clients
connected_clients:1
client_longest_output_list:0
client_biggest_input_buf:0
blocked_clients:0
```

客户端连接（密码方式）
```
# sh cli_with_password.sh
redis:6379> INFO Clients
# Clients
connected_clients:1
client_longest_output_list:0
client_biggest_input_buf:0
blocked_clients:0
```
