# Fluentd 正则示例

校验神器: [a Fluentd regular expression editor](http://fluentular.herokuapp.com)

## 示例1（Flask）

日志格式：
```
127.0.0.1 - - [19/Feb/2020 19:31:03] "GET /auth/index.html?next=%2F HTTP/1.1" 200 - INFO [_internal.py: 122 _log]
```
正则表达：
```
^(?<ip>[^ ]*) [^ ]* [^ ]* \[(?<time>[^\]]*)\] "(?<method>\S+)(?: +(?<path>[^ ]*) +\S*)?" (?<code>[^ ]*) [^ ]* (?<level>\S+) \[(?<file>[^:]*): (?<line>\d+) (?<fun>[^\]]*)\]?$
```
时间格式：
```
%d/%b/%Y %H:%M:%S
```

常用的日期格式：
```
%Y-%m-%d %H:%M:%S %z
```

## 示例2（Django）


## 示例3（Gin）


## 示例4（Nginx）
