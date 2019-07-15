# RabbitMQ

https://hub.docker.com/_/rabbitmq/
```
$ sudo docker pull rabbitmq:3.6.9
```

`rabbitmq/docker_run_management.sh`在`rabbitmq/docker_run.sh`的基础上，启用了管理插件


测试
```
python mq_receive_logs_topic.py "*.rabbit"
python mq_emit_log_topic.py red.rabbit Hello
```


## 故障排错

磁盘空间占满，服务重启失败
```
not_a_dets_file, "/var/lib/rabbitmq/mnesia/rabbit@rabbitmq/recovery.dets"
```
经查，`/var/lib/rabbitmq/mnesia/rabbit@rabbitmq/recovery.dets`文件为空，删除，重启即可

```
rm -f /var/lib/rabbitmq/mnesia/rabbit@rabbitmq/recovery.dets
```
