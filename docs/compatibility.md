## compatibility

compatibility for python2 and python3


```python
from __future__ import print_function
from __future__ import unicode_literals
```

```python
# from StringIO import StringIO     # PY2
# from io import StringIO           # PY3
from six import StringIO
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
