#!/usr/bin/env bash

docker run -d --net=host  --name=mon
    -v /etc/ceph:/etc/ceph
    -v /var/lib/ceph/:/var/lib/ceph
    -e MON_IP=192.168.8.106
    -e CEPH_PUBLIC_NETWORK=192.168.0.0/16
    ceph/daemon mon

# MON_IP就是宿主机的IP地址
