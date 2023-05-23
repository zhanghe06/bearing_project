# logging

Flask 使用的是 [python标准库的logging](https://docs.python.org/3/library/logging.html#module-logging)


Logging提供5个等级的输出，CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET；
如果把looger的级别设置为INFO， 那么小于INFO级别的日志都不输出， 大于等于INFO级别的日志都输出

## 组件

组件 | 介绍
--- | ---
Logger | 对象提供应用程序可直接使用的接口，供应用代码使用；
Handler | 发送日志到适当的目的地；
Filter | 提供了过滤日志信息的方法，控制输出； 
Formatter | 指定日志输出和显示的具体格式。


## 配置参数

logging.basicConfig()函数中的具体参数：

参数 | 解释
--- | ---
filename | 指定的文件名创建FiledHandler，这样日志会被存储在指定的文件中
filemode | 文件打开方式，在指定了filename时使用这个参数，默认值为“w”还可指定为“a”
format | 指定handler使用的日志显示格式
datefmt | 指定日期时间格式
level | 设置rootlogger的日志级别
stream | 用指定的stream创建StreamHandler。可以指定输出到sys.stderr,sys.stdout或者文件，默认为sys.stderr。若同时列出了filename和stream两个参数，则stream参数会被忽略


## format参数

format参数 | 说明
--- | ---
%(name)s | Logger的名字
%(levelno)s | 数字形式的日志级别
%(levelname)s | 文本形式的日志级别
%(pathname)s | 调用日志输出函数的模块的完整路径名，可能没有
%(filename)s | 调用日志输出函数的模块的文件名
%(module)s | 调用日志输出函数的模块名
%(funcName)s | 调用日志输出函数的函数名
%(lineno)d | 调用日志输出函数的语句所在的代码行
%(created)f | 当前时间，用UNIX标准的表示时间的浮 点数表示
%(relativeCreated)d | 输出日志信息时的，自Logger创建以 来的毫秒数
%(asctime)s | 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d | 线程ID。可能没有
%(threadName)s | 线程名。可能没有
%(process)d | 进程ID。可能没有
%(message)s | 用户输出的消息



flask 默认日志配置`flask/logging.py`
```
default_handler = logging.StreamHandler(wsgi_errors_stream)
default_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
)
```

## traceback

traceback.format_exc() 返回字符串，traceback.print_exc()则直接给打印出来
traceback.print_exc() 终端运行才会打印
