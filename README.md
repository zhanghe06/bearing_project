## 轴承行业 - 最佳实践

[![Build Status](https://travis-ci.org/zhanghe06/bearing_project.svg?branch=master)](https://travis-ci.org/zhanghe06/bearing_project)
[![Coverage Status](https://coveralls.io/repos/github/zhanghe06/bearing_project/badge.svg?branch=master)](https://coveralls.io/github/zhanghe06/bearing_project?branch=master)

项目目标

- [x] 客户管理
- [x] 产品管理
- [x] 员工管理
- [x] 报价管理
- [ ] 订单管理
- [x] 库存管理
- [ ] 财务管理
- [x] 会话管理
- [x] 消息管理
- [ ] 操作日志
- [ ] 系统日志
- [ ] 服务监控

系统依赖
- Nginx
- Redis
- MariaDB
- MongoDB


项目依赖
```bash
pip install Flask
pip install Flask-Login
pip install Flask-SQLAlchemy
pip install Flask-WTF
pip install Flask-OAuthlib
pip install Flask-Excel
pip install pyexcel-xls
pip install Flask-Principal
pip install Flask-Babel
pip install Flask-Moment
pip install Flask-Mail
pip install sqlacodegen==1.1.6  # 注意: 最新版 sqlacodegen==2.0 有bug
pip install gunicorn
pip install eventlet
pip install Flask-SocketIO
pip install Flask-WeasyPrint
pip install redis
pip install requests
pip install mysqlclient
pip install PyMongo
pip install Pillow
pip install elasticsearch
pip install user-agents
pip install six
pip install future
pip install supervisor      # 当前主版本3只支持py2，将来主版本4(未发布)会支持py3
```
因当前`supervisor`不支持`python3`，故在`requirements.txt`中将其去掉


## 项目演示
python2
```
virtualenv bearing.env
source env_develop.sh
pip install -r requirements.txt
python run_backend.py
```

python3
```
virtualenv bearing.env -p python3
source env_develop.sh
pip install -r requirements.txt
python run_backend.py
```


## 信息安全

- 接口请求次数限制
- 防止重放
- 防止越权


## 本地化、国际化

创建步骤
```bash
# 查看本机支持的语言
pybabel --list-locales

# 创建模板文件
pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .

# 创建模板文件(方式二)
pybabel extract \
    -F babel.cfg \
    --omit-header \
    -k lazy_gettext \
    -o messages.pot .

# 创建模板文件(方式三)
pybabel extract \
    -F babel.cfg \
    --copyright-holder=COPYRIGHT_HOLDER \
    --project=PROJECT_HOLDER \
    --version=VERSION_HOLDER \
    -k lazy_gettext \
    -o messages.pot .

# 创建翻译文件（注意translations在Flask项目目录下）
pybabel init -i messages.pot -d translations -l en
pybabel init -i messages.pot -d translations -l zh

# 编辑翻译文件

# 编译翻译文件
pybabel compile -d translations
```

更新步骤
```bash
# 重新生成模板
pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .

# 更新翻译文件
pybabel update -i messages.pot -d translations

# 编辑翻译文件（检查 fuzzy）

# 编译翻译文件
pybabel compile -d translations
```

注意:
- `Babel`插件, 中文为`zh`
- `Moment`插件, 中文为`zh-cn`
- `html`标签`lang`属性, 中文为`zh-CN`
- 由于表单类是在Flask上下文环境外定义的, 需要使用`lazy_gettext`


## 闪现消息

Flask 闪现消息`category`

category    |消息类型
------------|-----------
message     |any kind of message
error       |errors
info        |information
warning     |warnings


Bootstrap 状态类

Class       |描述
------------|-----------
.active     |鼠标悬停在行或单元格上时所设置的颜色
.success    |标识成功或积极的动作
.info       |标识普通的提示信息或动作
.warning    |标识警告或需要用户注意
.danger     |标识危险或潜在的带来负面影响的动作

https://v3.bootcss.com/css/

所以`Flask`在与`Bootstrap`结合时, `category`使用`Bootstrap`的状态类


## tips 支持换行

tips默认是不支持换行的, 需要`data-html`和`data-toggle`一起配合

```
<img src="{{ url_for('captcha.get_code', code_type='login') }}"
     data-html="true" data-toggle="tooltip" data-placement="top"
     rel="tooltip"
     title="看不清<br/>换一张"
     id="captcha_img"
     onclick="refresh_code();">
```

title 动态显示

```
span_obj.prop('title', 'new title').tooltip('fixTitle').tooltip('show');
```
如果仅仅修改title, 不会触发tooltip渲染


## 权限控制

控制目标
1. 同一浏览器，切换不同用户，身份、权限不同
2. 后台修改用户权限，被修改用户权限立即生效

权限分配
1. 系统管理角色，拥有用户管理、角色管理的权限；
2. 普通用户角色，用户产品管理、客户管理，报价管理的权限；


## Font Awesome

https://fontawesome.com/icons


## 自动补全搜索插件

autocomplete

typeahead


## 会话管理

user-agents, User Agents 解析库

https://pypi.python.org/pypi/user-agents/

Nginx 负载均衡模式, 当设置 login_manager.session_protection = 'strong', chrome 浏览器 Disa cache 时, 会话会断开


## 性能调优

Redis

`info` 查看 `connected_clients`

`client list` 查看客户端连接情况

```
127.0.0.1:6379> INFO Clients
# Clients
connected_clients:72
client_longest_output_list:0
client_biggest_input_buf:0
blocked_clients:0

127.0.0.1:6379> CLIENT LIST
...

127.0.0.1:6379> CONFIG GET timeout
1) "timeout"
2) "0"
```

## 消息推送

方案一、Flask-SSE

基于`redis`通过订阅发布实现
```
pip install gevent
pip install Flask-SSE
```
缺点: 项目停止维护、redis连接过多、消息推送导致用户退出登录（待查）


方案二、Flask-SocketIO

推荐、项目活跃

https://github.com/miguelgrinberg/Flask-SocketIO

https://flask-socketio.readthedocs.io/en/latest

https://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent


## JQuery 注意动态加载元素事件绑定

直接在动态元素上绑定事件无法实现, 需要通过以下形式在父元素或`body`上绑定事件
```
$('body').on('click', '.class-name', function(){
  $('.sub-class-name').each(function () {
    $(this).click()
  })
})
```

## H5 兼容PC、移动端点击事件

需要区分平台, 分别绑定对应事件
```javascript
$(function () {
    var is_mobile = window.hasOwnProperty("ontouchstart")
    var toggle_password_obj = $('#toggle_password')
    var captcha_img_obj = $('#captcha_img')

    if(is_mobile){
        toggle_password_obj.bind('touchstart', toggle_password)
        captcha_img_obj.bind('touchstart', refresh_code)
    }else {
        toggle_password_obj.bind('click', toggle_password)
        captcha_img_obj.bind('click', refresh_code)
    }
})
```

如果仅仅绑定`click`, 移动端初次点击, 需要点击两次

如果同时绑定`touchstart`和`click`, 移动端会触发两次事件


## 关于 cli 模式下的上下文管理

cli 模式下, 需要加入如下代码
```
ctx = app.app_context()
ctx.push()
```
或者
```
with app.app_context():
    ...
    pass
```

参考:

[when-scattering-flask-models-runtimeerror-application-not-registered-on-db-w](https://stackoverflow.com/questions/19437883/when-scattering-flask-models-runtimeerror-application-not-registered-on-db-w)

[flask-create-app-and-setup-unittest](https://stackoverflow.com/questions/48353929/flask-create-app-and-setup-unittest)


## 关于 mysql python 客户端的选择

https://pypi.org/project/mysqlclient/

`mysqlclient`在`MySQL-python`的基础上，新增了对`py3`的支持并修复了一些bug


## MySQL 字段区分大小写

字符型字段默认是不区分大小写，若想区分，需要指定 BINARY

为登录账号、密码字段设置大小写敏感
```
`auth_key` VARCHAR(60) BINARY
`auth_secret` VARCHAR(60) BINARY
```
或
```
`auth_key` VARBINARY(60)
`auth_secret` VARBINARY(60)
```


## Flask-Mail

https://pythonhosted.org/Flask-Mail/


## 系统日志 和 服务监控



## eventlet VS gevent

```
import eventlet
eventlet.monkey_patch()
```
```
from gevent import monkey
monkey.patch_all()
```


## Nginx

如果前端有CDN内容分发存在, ip_hash方式就没有意义了

## ES IK 热词更新

```
<!--用户可以在这里配置远程扩展字典 -->
<entry key="remote_ext_dict">location</entry>
<!--用户可以在这里配置远程扩展停止词字典-->
<entry key="remote_ext_stopwords">location</entry>
```

1. 该 http 请求需要返回两个头部(header)，一个是 Last-Modified，一个是 ETag，这两者都是字符串类型，只要有一个发生变化，该插件就会去抓取新的分词进而更新词库。
2. 该 http 请求返回的内容格式是一行一个分词，换行符用 \n 即可。

满足上面两点要求就可以实现热更新分词了，不需要重启 ES 实例。


## WTForms FieldList

http://wtforms.readthedocs.io/en/stable/fields.html#wtforms.fields.FieldList

明细表单如需取消`csrf_token`, 明细表单需要继承`wtforms.Form`, 而不是`flask_wtf.FlaskForm`

或者
```python
from flask_wtf import FlaskForm
class SomeForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        FlaskForm.__init__(self, *args, **kwargs)
```

注意: 嵌套表单不能有`name`字段, `form.name`表示嵌套表单明细的名称


## WTForms

https://github.com/wtforms/wtforms/blob/79840898a3e17b0ae535d9fdcff9537ef0e190b0/CHANGES.rst#version-22

Version 2.2 新增了`required`属性的渲染, 注意: `hidden`类型的文本框不会校验`required`属性


## 本地事务的幂等性

- select，天生幂等
- insert，数据库自增主键时不具备幂等
- 基于主键update，具备幂等，但是带查询的更新除外（形如update t set x = x + 1 where ...)
- 基于主建delete，具备幂等
- 非基于主键的udpate/delete操作，需要具体问题具体分析


## MariaDB datetime 类型

https://mariadb.com/kb/en/library/datetime/

The supported range is '1000-01-01 00:00:00.000000' to '9999-12-31 23:59:59.999999'


## Lazy Loading

http://docs.jinkan.org/docs/flask/patterns/lazyloading.html


## 引入的js文件中如果包含`jinja`标签, 需要使用`include`方法

```
{% block javascript %}
    <script type="text/javascript">
        {% include "myscript.js" %}
    </script>
    <!-- The contents of myscript.js will be loaded inside the script tag -->
{% endblock %}
```

## Flask-WeasyPrint

系统依赖

https://weasyprint.readthedocs.io/en/latest/install.html

ubuntu
```
sudo apt-get install libpango1.0-0
sudo apt-get install libcairo2
sudo apt-get install libpq-dev
```

mac
```
brew install cairo pango gdk-pixbuf libffi
```

## 外链设计

```html
<a target="_blank" href="https://link.juejin.im?target=https%3A%2F%2Fswagger.io" rel="nofollow noopener noreferrer">Swagger</a>
```


## TODO

- [x] 联动删除
- [x] 批量删除
- [ ] 输入清空
- [ ] 状态通知
- [ ] 导入检测
- [x] 复制单据
- [ ] 资源版本
- [ ] 防止盗链
- [ ] 库存移位
- [ ] 滚动升级
- [ ] 性能测试
- [ ] 压力测试
- [x] 打印页面
