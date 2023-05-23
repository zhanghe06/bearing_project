# Consul

[https://hub.docker.com/_/consul](https://hub.docker.com/_/consul)

[https://github.com/hashicorp/consul](https://github.com/hashicorp/consul)

## 架构

[https://www.consul.io/docs/architecture](https://www.consul.io/docs/architecture)

## 

```
CONSUL_HTTP_ADDR=127.0.0.1:8500
CONSUL_HTTP_TOKEN=aba7cbe5-879b-999a-07cc-2efd9ac0ffe
CONSUL_HTTP_AUTH=operations:JPIMCmhDHzTukgO6
```

注册服务
```
curl -X PUT -d '
{
    "id": "api-server-01",
    "name": "api-server-01",
    "address": "127.0.0.1",
    "tags": [
        "api"
    ],
    "port": 8180
}
' http://127.0.0.1:8500/v1/agent/service/register
```

注销服务
```
curl -X PUT http://127.0.0.1:8500/v1/agent/service/deregister/api-server-01
```

查看注册服务
```
curl http://<consul_ip>:8500/v1/agent/services?pretty
```

批量注销服务
```
curl -s http://<consul_ip>:8500/v1/agent/services | python3 -q -m json.tool | grep '"ID": "<service_ip>:' | awk -F '"' '{print "curl -X PUT http://<consul_ip>:8500/v1/agent/service/deregister/"$4}' | sh
```

## 集群
