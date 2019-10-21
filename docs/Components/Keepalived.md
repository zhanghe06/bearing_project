# Keepalived

keepalived是以VRRP协议为实现基础的，VRRP全称Virtual Router Redundancy Protocol，即虚拟路由冗余协议

keepalived默认使用端口122进行通讯,必须开放112端口,或者停用防火墙.保证各个主机之间112端口的连通性

```
node1   192.168.64.133       # master
node2   192.168.64.134       # backup
vip     192.168.64.130
```

```
# vim /etc/hosts
192.168.64.133 node1
192.168.64.134 node2
# ping -c 4 node1
# ping -c 4 node2
```

```
# yum install -y keepalived
# systemctl enable keepalived
# systemctl status keepalived
# cp /etc/keepalived/keepalived.conf /etc/keepalived/keepalived.conf.bak
```

master
```
global_defs {
   router_id node1
}

vrrp_instance VI_1 {
    state MASTER
    interface ens33
    virtual_router_id 51
    priority 150
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.64.130
    }
}
```


backup
```
global_defs {
   router_id node2
}

vrrp_instance VI_1 {
    state BACKUP
    interface ens33
    virtual_router_id 51
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.64.130
    }
}
```

```
# systemctl restart keepalived
# systemctl status keepalived
# ping -c 4 192.168.64.130
```

配置路由转发

临时
```
# echo 1 > /proc/sys/net/ipv4/ip_forward
```
永久
```
# echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.d/99-sysctl.conf 
# sysctl -p
```

修改防火墙
```
# systemctl stop firewalld
# systemctl disable firewalld
```
或者，下面（没试）
```
# systemctl status firewalld
# firewall-cmd --direct --permanent --add-rule ipv4 filter INPUT 0 --in-interface ens33 --destination 192.168.64.130 --protocol vrrp -j ACCEPT
# firewall-cmd --direct --permanent --add-rule ipv4 filter OUTPUT 0 --out-interface ens33 --destination 192.168.64.130 --protocol vrrp -j ACCEPT
# firewall-cmd --reload
```
