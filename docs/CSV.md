# CSV

中文乱码解决方案

将`codecs.BOM_UTF8`加到文件字节的头部

```
import codecs

codecs.BOM_UTF8 + csv_bytes...
```

注意，如果非字节形式，则需要添加`\ufeff`
```
'\ufeff' + csv_string...
```
