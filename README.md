## 轴承行业 - 最佳实践

[![Build Status](https://travis-ci.org/zhanghe06/bearing_project.svg?branch=master)](https://travis-ci.org/zhanghe06/bearing_project)
[![Coverage Status](https://coveralls.io/repos/github/zhanghe06/bearing_project/badge.svg?branch=master)](https://coveralls.io/github/zhanghe06/bearing_project?branch=master)

项目目标

- [ ] 客户管理
- [ ] 产品管理
- [ ] 员工管理
- [ ] 报价管理
- [ ] 订单管理
- [ ] 库存管理
- [X] 会话管理
- [X] 消息管理
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
pip install sqlacodegen
pip install gunicorn
pip install eventlet
pip install Flask-SocketIO
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


## 关于 cli 模式下的上下文管理

cli 模式下, 需要加入如下代码
```
ctx = app.app_context()
ctx.push()
```

参考:

[when-scattering-flask-models-runtimeerror-application-not-registered-on-db-w](https://stackoverflow.com/questions/19437883/when-scattering-flask-models-runtimeerror-application-not-registered-on-db-w)

[flask-create-app-and-setup-unittest](https://stackoverflow.com/questions/48353929/flask-create-app-and-setup-unittest)


## 关于 mysql python 客户端的选择

https://pypi.org/project/mysqlclient/

`mysqlclient`在`MySQL-python`的基础上，新增了对`py3`的支持并修复了一些bug


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
