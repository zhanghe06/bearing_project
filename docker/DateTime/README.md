# DateTime

测试容器终端日志

```
docker inspect --format='{{.LogPath}}' <containername>                      # json-file模式下有返回值
docker inspect --format='{{.HostConfig.LogConfig.Type}}' <containername>    # 当前 container logging driver
docker info --format='{{.LoggingDriver}}'                                   # dockerd 默认 logging driver
```
