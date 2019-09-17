# DateTime

- UTC
- ISO8601
    - 24小时制
    - 字母T分割日期和时间
    - Z表示UTC时间

以下表示同一时刻

时间描述 | 格式表达 | 时区
--- | --- | ---
北京时间 2019-01-01 09:30:00 | 2019-01-01T09:30:00+08:00 | 东8区
北京时间 2019-01-01 09:30:00 | 2019-01-01T01:30:00+00:00 | 0时区
北京时间 2019-01-01 09:30:00 | 2019-01-01T01:30:00Z | UTC时间

数据库 timestamp 格式，经过 sqlalchemy orm 转换之后，变成 DateTime 格式


## unix时间戳

时间戳是指格林威治时间1970年01月01日00时00分00秒(北京时间1970年01月01日08时00分00秒)起至现在的总毫秒数

```ipython
In [1]: import time

In [2]: time.mktime(time.localtime())
Out[2]: 1568280373.0

In [3]: time.mktime(time.strptime('1970-01-01 08:00:00', '%Y-%m-%d %H:%M:%S'))
Out[3]: 0.0

In [4]: time.mktime(time.strptime('2019-01-01 08:00:00', '%Y-%m-%d %H:%M:%S'))
Out[4]: 1546300800.0
```
如果转时间戳，必须是本地时间

## moment.js

以下以北京时间 2019-01-01 08:00:00 为例

```javascript
moment.unix(1546300800).format()
"2019-01-01T08:00:00+08:00"

moment.unix(1546300800).utc().format()
"2019-01-01T00:00:00Z"

moment("2019-01-01 08:00:00").format()
"2019-01-01T08:00:00+08:00"

moment("2019-01-01T00:00:00Z").format()
"2019-01-01T08:00:00+08:00"
```

1. 使用正确的时间戳
2. 使用ISO8601格式的UTC时间

## Flask-Moment

Flask-Moment 扩展核心源码

bearing.env/lib/python2.7/site-packages/flask_moment.py
```python
class _moment(object):
    ...
    def __init__(self, timestamp=None, local=False):
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp
        self.local = local

    def _timestamp_as_iso_8601(self, timestamp):
        tz = ''
        if not self.local:
            tz = 'Z'
        return timestamp.strftime('%Y-%m-%dT%H:%M:%S' + tz)
```

所以数据库只需存储UTC时间即可

```ipython
In [1]: from datetime import datetime

In [2]: datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
Out[2]: '2019-09-12T17:02:39Z'

In [3]: datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
Out[3]: '2019-09-12T09:02:42Z'
```
