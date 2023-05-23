## Compatibility

compatibility for python2 and python3

- six: python2的写法，兼容python3
- future: python3的写法，兼容python2

[https://python-future.org/compatible_idioms.html](https://python-future.org/compatible_idioms.html)

```python
from __future__ import print_function
from __future__ import unicode_literals
```

```python
# from StringIO import StringIO     # PY2
# from io import StringIO           # PY3
from six import StringIO
# 可以用字节方式替代:
from io import BytesIO
from six import BytesIO
```

```python
# from HTMLParser import HTMLParser     # PY2
# from html.parser import HTMLParser    # PY3
from future.moves.html.parser import HTMLParser
```

```python
# from urlparse import urljoin                  # PY2
# from urllib.parse import urljoin              # PY3
from future.moves.urllib.parse import urljoin
```

```python
# from urlparse import urlparse, urlunparse, parse_qsl                              # PY2
# from urllib import urlencode                                                      # PY2
# from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode               # PY3
from future.moves.urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
```

```python
# from urllib import quote                      # PY2
# from urllib.parse import quote                # PY3
from future.moves.urllib.parse import quote
```

```python
# PY2(raw_input)
# PY3(input)
from future.builtins import input
```

```python
# PY2(iteritems)
# PY3(items)
from six import iteritems, iterkeys, itervalues
```

```python
# PY2(xrange)
# PY3(range)
from future.builtins import range
from past.builtins import xrange
```

```python
import six

# six.string_types = (str, unicode)
# six.integer_types = (int, long)
# six.class_types = (type, types.ClassType)
# six.text_type = unicode
# six.binary_type = str

# six.b
# six.u

# def b(s: str) -> binary_type: ...
# def u(s: str) -> text_type: ...
```

```python
unichr(i)               # PY2
chr(i)                  # PY3

from six import unichr
unichr(i)
```

继承类
```python
# python2
class MainClass(object):
    def __init__(self, *args, **kwargs):
        pass


class SubClass(MainClass):
    def __init__(self, *args, **kwargs):
        super(SubClass, self).__init__(*args, **kwargs)

# python3
class MainClass(object):
    def __init__(self, *args, **kwargs):
        pass


class SubClass(MainClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# 兼容
class MainClass(object):
    def __init__(self, *args, **kwargs):
        pass


class SubClass(MainClass):
    def __init__(self, *args, **kwargs):
        MainClass.__init__(self)
```

抽象类
```python
# python2
import abc
class SomeAbstractClass(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def do_something(self):
        pass

# python3
import abc
class SomeAbstractClass(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def do_something(self):
        pass
```

元类
```python
class MetaClass(type):  # 只有继承了type类才能称之为一个元类，否则就是一个普通的自定义类
    def __init__(self, class_name, class_bases, class_dic):
        print(self)  # 现在是People
        print(class_name)
        print(class_bases)
        print(class_dic)
        super(MetaClass,self).__init__(class_name, class_bases, class_dic)  # 重用父类的功能

# python2


# python3


# 兼容
import six

@six.add_metaclass(MetaClass)
class SomeClass(object):
    pass
```
