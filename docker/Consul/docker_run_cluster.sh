#!/usr/bin/env bash

# 服务模式

# 容错能力：3节点集群可以容忍1个节点失效；5节点集群可以容忍2个节点失效

docker run -d --name=consul-s1 -e CONSUL_BIND_INTERFACE=eth0 -p 8500:8500 consul agent -bootstrap-expect=3 -server=true -client=0.0.0.0 -node=server-1 -ui

IP=`docker inspect --format="{{.NetworkSettings.Networks.bridge.IPAddress}}" consul-s1`

docker run -d --name=consul-s2 -e CONSUL_BIND_INTERFACE=eth0 consul agent -bootstrap-expect=3 -server=true -client=0.0.0.0 -node=server-2 -join=${IP}

docker run -d --name=consul-s3 -e CONSUL_BIND_INTERFACE=eth0 consul agent -bootstrap-expect=3 -server=true -client=0.0.0.0 -node=server-3 -join=${IP}

# docker exec -t consul-s1 consul members

# http://127.0.0.1:8500/ui/

# 客户模式
docker run -d --name=consul-c1 -e CONSUL_BIND_INTERFACE=eth0 consul agent -server=false -client=0.0.0.0 -node=client-1 -join=${IP}

docker run -d --name=consul-c2 -e CONSUL_BIND_INTERFACE=eth0 consul agent -server=false -client=0.0.0.0 -node=client-2 -join=${IP}

docker run -d --name=consul-c3 -e CONSUL_BIND_INTERFACE=eth0 consul agent -server=false -client=0.0.0.0 -node=client-3 -join=${IP}

docker exec -t consul-s1 consul members

# curl http://localhost:8500/v1/health/service/consul?pretty
# curl http://localhost:8500/v1/catalog/nodes?pretty

# docker rm -f consul-c3 consul-c2 consul-c1
# docker rm -f consul-s3 consul-s2 consul-s1
