# Consul

[https://hub.docker.com/_/consul](https://hub.docker.com/_/consul)

[https://github.com/hashicorp/consul](https://github.com/hashicorp/consul)

##

```
CONSUL_HTTP_ADDR=127.0.0.1:8500
CONSUL_HTTP_TOKEN=aba7cbe5-879b-999a-07cc-2efd9ac0ffe
CONSUL_HTTP_AUTH=operations:JPIMCmhDHzTukgO6
```

查看注册服务
```
curl http://<consul_ip>:8500/v1/agent/services
```

批量注销服务
```
curl -s http://<consul_ip>:8500/v1/agent/services | python3 -q -m json.tool | grep '"ID": "<service_ip>:' | awk -F '"' '{print "curl -X PUT http://<consul_ip>:8500/v1/agent/service/deregister/"$4}' | sh
```
