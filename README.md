## 轴承行业 - 最佳实践

项目目标

- [ ] 客户管理
- [ ] 产品管理
- [ ] 员工管理
- [ ] 报价管理
- [ ] 订单管理
- [ ] 库存管理

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
pip install supervisor
pip install redis
pip install requests
pip install MySQL-python
pip install PyMongo
pip install Pillow
pip install elasticsearch
pip install six
pip install future
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

