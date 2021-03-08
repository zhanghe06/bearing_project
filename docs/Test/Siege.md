# Siege 压力测试


测试指标 | 测试描述
--- | ---
Transactions | 事务命中次数
Availability | 请求处理成功比例
Elapsed time | 测试持续时间
Data transferred | 传输数据总和
Response time | 平均响应时间
Transaction rate | 事务处理效率
Throughput | 吞吐量
Concurrency | 并发连接数量
Successful transactions | 成功事务次数
Failed transactions | 失败事务次数
Longest transaction | 最长事务时间
Shortest transaction | 最短事务时间



100并发，发生2次
```
$ siege -c 100 -r 2 http://0.0.0.0:8010/performance/ -b
```

Flask 自带的web服务
```
Transactions:                200 hits
Availability:             100.00 %
Elapsed time:               3.21 secs
Data transferred:           0.00 MB
Response time:              0.95 secs
Transaction rate:          62.31 trans/sec
Throughput:             0.00 MB/sec
Concurrency:               59.36
Successful transactions:         200
Failed transactions:               0
Longest transaction:            1.55
Shortest transaction:           0.15
```

Gunicorn
```
Transactions:               200 hits
Availability:             100.00 %
Elapsed time:               1.66 secs
Data transferred:           0.00 MB
Response time:              0.34 secs
Transaction rate:         120.48 trans/sec
Throughput:             0.00 MB/sec
Concurrency:               40.89
Successful transactions:         200
Failed transactions:               0
Longest transaction:            0.66
Shortest transaction:           0.04
```

Gunicorn 性能也只是 Flask 自带服务的一倍



```
siege -c 200 -r 100 -b http://0.0.0.0:8010/performance/
```

Flask 自带的web服务
```
Transactions:		       19856 hits
Availability:		       99.28 %
Elapsed time:		      418.45 secs
Data transferred:	        0.08 MB
Response time:		        2.61 secs
Transaction rate:	       47.45 trans/sec
Throughput:		        0.00 MB/sec
Concurrency:		      123.84
Successful transactions:       19856
Failed transactions:	         144
Longest transaction:	       83.56
Shortest transaction:	        0.01
```

Gunicorn
```
Transactions:		       19930 hits
Availability:		       99.65 %
Elapsed time:		      187.44 secs
Data transferred:	        0.08 MB
Response time:		        1.08 secs
Transaction rate:	      106.33 trans/sec
Throughput:		        0.00 MB/sec
Concurrency:		      114.35
Successful transactions:       19930
Failed transactions:	          70
Longest transaction:	      117.82
Shortest transaction:	        0.01
```
