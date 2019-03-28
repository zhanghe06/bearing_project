## Docker

Docker的监控原则：
根据docker官方声明，一个容器不建议跑多个进程，所以不建议在容器中使用agent进行监控（zabbix等），agent应该运行在宿主机，通过cgroup或是docker api获取监控数据。
