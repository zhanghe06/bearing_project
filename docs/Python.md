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


### 三、导入库函数

导入分组顺序：  
1、标准库导入  
2、有关的第三方库进口  
3、本地应用程序/库特定的导入


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

原理：  
list 为可变类型，当第一次删除后，后面的元素会前移  
for 遍历 list 时，如果遍历过程中此 list 变化，会产生非预期的结果


### 5、浅拷贝(copy.copy)和深拷贝(copy.deepcopy)

如果对象本身是不可变的，那么浅拷贝时也会产生两个值  
顺便回顾下 Python 标准类型的分类：
- 可变类型： 列表，字典
- 不可变类型：数字，字符串，元组


### 6、列表转字典
```
In [1]: lk = ['a', 'b', 'c']

In [2]: lv = ['1', '2', '3']

In [3]: dict(zip(lk, lv))
Out[3]: {'a': '1', 'b': '2', 'c': '3'}
```

### 7、对象类型判断
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


### 8、类的多继承、混入

### 9、接口

### 10、元类

## Python2 和 Python3 兼容

比如第三方库 pandas，以下是 Python2 最后一个版本
```bash
pip install numpy==1.16.4
pip install pandas==0.24.2
```
其中 numpy 是 pandas 的依赖库，需要同步 Python2 版本，后续版本不在支持 Python2
