# Flask-Excel

中文乱码

```
import codecs
response.content = codecs.BOM_UTF8 + response.content
```
Flask、Django 均适用，可在中间件统一处理
