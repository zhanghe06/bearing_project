# 第三方 Token 管理

## 通过延迟队列设计

```
                                      |-------------- ReQueue ------------|
Token 01 -|                           v                                   |                         |-  Record 01
Token 02 -| ->  Platform A  ->  (Delay Queue)     (Work Queue)  ->  Worker Process   ->   [DB]  ->  |-  Record 02
Token 03 -|                           |                ^                 ...                        |-  Record 03
                                      |---- Expire ----|

                                      |-------------- ReQueue ------------|
Token 04 -|                           v                                   |                         |-  Record 04
Token 05 -| ->  Platform B  ->  (Delay Queue)     (Work Queue)  ->  Worker Process   ->   [DB]  ->  |-  Record 05
Token 06 -|                           |                ^                 ...                        |-  Record 06
                                      |---- Expire ----|
```

延迟队列的过期时间必须小于Token计划过期时间

工作进程刷新完Token写入数据库之后，需将带上过期时间的Token标识重新入队


## 通过 ETCD 方案设计
