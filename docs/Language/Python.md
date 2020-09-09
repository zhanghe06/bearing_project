# Python

设计模式:  
[https://github.com/faif/python-patterns](https://github.com/faif/python-patterns)

攻略:  
[http://blog.hszofficial.site/TutorialForPython/](http://blog.hszofficial.site/TutorialForPython/)


## 编码规范

Python代码规范，请看PEP 8的官方文档：  
[https://www.python.org/dev/peps/pep-0008/](https://www.python.org/dev/peps/pep-0008/)

### 一、编码风格

#### 1、缩进

每个缩进级别使用4个空格，禁用制表符。


#### 2、空格

运算符两边空1格；例外：函数参数赋默认值=两边不用空格

注释#后跟一个空格；如果注释跟在代码行右边，#前使用2个空格分隔

逗号、冒号前面不要空格；参数分隔符逗号、字典键值对冒号后面跟1个空格；函数定义尾部冒号前后不要空格

#### 3、空白行

类内方法，空1行分隔

顶层函数和类，空2行分隔

一行只import一个包，Imports的顺序为：标准库、相关主包、特定应用，每组导入之间放置1行空行，所有导入使用包的绝对路径。

#### 4、每行代码的最大长度

每行不要超过80个字符

Python标准库是保守的，需要将行限制为79个字符（文档字符串/注释为72）。

如果一个文本字符串在一行放不下, 可以使用圆括号来实现隐式行连接:
```
x = ('这是一个非常长非常长非常长非常长 '
     '非常长非常长非常长非常长非常长非常长的字符串')
```


### 二、命名约定

#### 1、变量名

蛇形
```
my_list = [
    1, 2, 3,
    4, 5, 6,
]
```

#### 2、方法名

蛇形
```
def my_func():
    pass
```

#### 3、类名

大驼峰
```
class MyClass(object):
    def __init__(self):
        pass
```
python3 不用继承 object，默认就是新式类


### 三、包和模块

#### 导入分组顺序：  
1、标准库导入  
2、有关的第三方库进口  
3、本地应用程序/库特定的导入

#### 导入全部
注意: `from test_module import *` 仅仅支持包级别导入，不能用于方法中

#### 相对引用
from ..database import db_session 这样的写法是显式相对引用, 这种引用方式只能用于 package 中, 而不能用于主模块中。  
因为主 module 的 name 总是为 main , 并没有层次结构, 也就无从谈起相对引用了。  
换句话, if __name__=="__main__": 和相对引用是不能并存的。


### Python 的 IDE(PyCharm) 配置 PEP 8 规范

```
Preferences... -> Editor -> Inspections -> Python -> 勾选2项（编码风格、命名约定）: PEP 8 coding style violation; PEP 8 naming convention violation
```


## 语法进阶


### 1、理解元祖
```
In [1]: type((1))
Out[1]: int

In [2]: type((1,))
Out[2]: tuple
```
单元素元祖，元素后需要跟一个逗号


### 2、多值匹配
已知：content_type 为字符串，search 为字符串元素组成的列表  
检查 content_type 是否存在 search 中任意一个元素
```
In [1]: search = ['image', 'png', 'jpg', 'jpeg', 'webp']

In [2]: content_type = 'image/png'

In [3]: result = [x in content_type for x in search].count(True)

In [4]: result
Out[4]: 2
```


### 3、等长列表对应元素运算
```
In [1]: list(map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10]))
Out[1]: [3, 7, 11, 15, 19]
```

Python map() 函数
- Python 2.x 返回列表
- Python 3.x 返回迭代器


### 4、列表遍历删除

错误方式
```
In [1]: a = [2, 4, 6, 8, 10]
   ...: for i in a:
   ...:     # print(i, a)
   ...:     if i % 2 == 0:
   ...:         a.remove(i)
   ...: a
Out[1]: [4, 8]
```

正确姿势
```
In [1]: a = [2, 4, 6, 8, 10]
    ...: for i in a[:]:
    ...:     # print(i, a)
    ...:     if i % 2 == 0:
    ...:         a.remove(i)
    ...: a
Out[1]: []
```
复制原始列表（切片、copy 方式均可）

对于列表的切片复制方式:
`[:]`和`[::]`效果一样

原理：  
list 为可变类型，当第一次删除后，后面的元素会前移  
for 遍历 list 时，如果遍历过程中此 list 变化，会产生非预期的结果


### 5、字典

判断字典中的键是否存在
```
>>> d = {'a': 1}
>>> d.has_key('a')
True
>>> 'a' in d
True
```
注意：`has_key`已经废弃，直接用`in`来判断


### 6、浅拷贝(copy.copy)和深拷贝(copy.deepcopy)

Python 中的对象之间赋值时是按引用传递的，如果需要拷贝对象，需要使用标准库中的 copy 模块。
1. copy.copy 浅拷贝 只拷贝父对象，不会拷贝对象的内部的子对象。
2. copy.deepcopy 深拷贝 拷贝对象及其子对象。

如果对象本身是不可变的，那么浅拷贝时也会产生两个值  
顺便回顾下 Python 标准类型的分类：
- 可变类型： 列表，字典
- 不可变类型：数字，字符串，元组


### 7、列表转字典
```
In [1]: lk = ['a', 'b', 'c']

In [2]: lv = ['1', '2', '3']

In [3]: dict(zip(lk, lv))
Out[3]: {'a': '1', 'b': '2', 'c': '3'}
```

### 8、对象类型判断
```
In [1]: import datetime
   ...:
   ...:
   ...: def show_datetime(obj):
   ...:     if isinstance(obj, datetime.datetime):
   ...:         return obj.strftime('%Y-%m-%d %H:%M:%S')
   ...:     elif isinstance(obj, datetime.date):
   ...:         return obj.strftime('%Y-%m-%d')
   ...:     else:
   ...:         raise TypeError('%r is not JSON serializable' % obj)
   ...:
   ...:
   ...: show_datetime(datetime.datetime.now())
Out[1]: '2019-07-26 13:39:21'
```
类型判断使用 isinstance


### 9、类的多继承、混入

### 10、接口

### 11、元类

1、什么是元类
```
在python中一切皆对象，那么我们用class关键字定义的类本身也是一个对象
负责产生该对象的类称之为元类，即元类可以简称为类的类

class Foo: # Foo=元类()        #一切皆对象，类加括号产生对象
    pass
```

2、为何要用元类
```
元类是负责产生类的，所以我们学习元类或者自定义元类的目的
是为了控制类的产生过程，还可以控制对象的产生过程
```

3、如何用元类

### 12、多进程、多线程、协程、本地线程

本地线程的意义：每个子线程使用全局对象a，但每个线程定义的属性a.xx是该线程独有的，避免变量的到处传递


## Python2 和 Python3 兼容

比如第三方库 pandas，以下是 Python2 最后一个版本
```bash
pip install numpy==1.16.4
pip install pandas==0.24.2
```
其中 numpy 是 pandas 的依赖库，需要同步 Python2 版本，后续版本不在支持 Python2


## 关键字

python2
```
➜  ~ python2
Python 2.7.15 (default, Aug 17 2018, 22:39:05)
[GCC 4.2.1 Compatible Apple LLVM 9.1.0 (clang-902.0.39.2)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> help("keywords")

Here is a list of the Python keywords.  Enter any keyword to get more help.

and                 elif                if                  print
as                  else                import              raise
assert              except              in                  return
break               exec                is                  try
class               finally             lambda              while
continue            for                 not                 with
def                 from                or                  yield
del                 global              pass

>>>
```

python3
```
➜  ~ python3
Python 3.6.5 (default, Apr 25 2018, 14:23:58)
[GCC 4.2.1 Compatible Apple LLVM 9.1.0 (clang-902.0.39.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> help("keywords")

Here is a list of the Python keywords.  Enter any keyword to get more help.

False               def                 if                  raise
None                del                 import              return
True                elif                in                  try
and                 else                is                  while
as                  except              lambda              with
assert              finally             nonlocal            yield
break               for                 not
class               from                or
continue            global              pass

>>>
```


## 调试运行中的进程

```
strace -p [PID]
```

```
-tt 在每行输出的前面，显示毫秒级别的时间
-T 显示每次系统调用所花费的时间
-v 对于某些相关调用，把完整的环境变量，文件stat结构等打出来。
-f 跟踪目标进程，以及目标进程创建的所有子进程
-e 控制要跟踪的事件和跟踪行为,比如指定要跟踪的系统调用名称
-o 把strace的输出单独写到指定的文件
-s 当系统调用的某个参数是字符串时，最多输出指定长度的内容，默认是32个字节
-p 指定要跟踪的进程pid, 要同时跟踪多个pid, 重复多次-p选项即可。
```

调试实践
```
strace -s 10240 -p <PID> -t -y -v
cat /proc/<PID>/fd/<fd_id>
lsof -p <PID> | grep <socket_id>
```

## 系统负载

```
uptime
 14:31:27 up 5 days, 23:52,  2 users,  load average: 0.37, 0.50, 0.25
```

load average 平均负载，这个一段时间一般取1分钟、5分钟、15分钟，需要和cpu（总线程数）对比


```
# 核心数
cat /proc/cpuinfo | grep "core id" | uniq | wc -l
# 线程数
cat /proc/cpuinfo | grep "processor" | wc -l
# 列出所有核心主频
cat /proc/cpuinfo |grep "cpu MHz"
```

MacOS 查看CPU
```
# 查看品牌，例如：Intel(R) Core(TM) i7-4870HQ CPU @ 2.50GHz
sysctl -n machdep.cpu.brand_string

# 核心数
sysctl -n machdep.cpu.core_count

# 线程数
sysctl -n machdep.cpu.thread_count
```


## `__new__`、`__init__` 区别

1. 首先用法不同
```
__new__()用于创建实例，所以该方法是在实例创建之前被调用，它是类级别的方法，是个静态方法；
__init__() 用于初始化实例，所以该方法是在实例对象创建后被调用，它是实例级别的方法，用于设置对象属性的一些初始值。
由此可知，__new__()在__init__() 之前被调用。如果__new__() 创建的是当前类的实例，会自动调用__init__()函数，通过return调用的__new__()的参数cls来保证是当前类实例，如果是其他类的类名，那么创建返回的是其他类实例，就不会调用当前类的__init__()函数。
```

2. 其次传入参数不同:
```
__new__()至少有一个参数cls，代表当前类，此参数在实例化时由Python解释器自动识别；
__init__()至少有一个参数self，就是这个__new__()返回的实例，__init__()在__new__()的基础上完成一些初始化的操作。
```

3. 返回值不同:
```
__new__()必须有返回值，返回实例对象；
__init__()不需要返回值。
```

## 序列化与反序列化

`encode`、`decode`

python3中
```
encode 输出字节串
decode 输出字符串
```

```
>>> a = '编码'
>>> a
'编码'
>>> b = a.encode('utf-8')
>>> b
b'\xe7\xbc\x96\xe7\xa0\x81'
>>> b.decode('utf-8')
'编码'
```

pickle.dumps() 将python数据序列化为bytes类型
pickle.loads() 将bytes类型数据反序列化为python的数据类型
