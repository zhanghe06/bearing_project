# FlaskBB

## 板块结构
- 版块 Category
- 论坛 Forum
- 主题 Topic
- 帖子 Posts (包含: 回复 Reply)

- 会员 Member
- 分组 Group
    - 管理员
    - 超级版主
    - 版主
    - 会员
    - 封禁

```
git https://github.com/zhanghe06/forum_project.git
cd forum_project
git checkout 2.0.0
```

创建虚拟环境
```
virtualenv .venv
source .venv/bin/activate
```

安装依赖
```
pip install Flask
pip install Flask-Alembic
pip install flask-allows
pip install Flask-BabelPlus
pip install Flask-Caching
pip install Flask-DebugToolbar
pip install Flask-Limiter
pip install Flask-Login
pip install Flask-Mail
pip install Flask-Redis
pip install Flask-SQLAlchemy
pip install Flask-Themes2
pip install flask-whooshee
pip install Flask-WTF
pip install flaskbb-plugin-conversations
pip install flaskbb-plugin-portal
pip install mysqlclient
pip install uwsgi
pip install supervisor
```

新增 flaskbb.cfg

mkdir -p uploads logs

supervisord
supervicorctl start all




```
make dependencies
flaskbb makeconfig
```

flaskbb makeconfig 交互过程(指定mysql数据源)：
```
(.venv) ➜  flaskbb git:(2.0.0) flaskbb makeconfig
The path to save this configuration file.
Save to [/Users/zhanghe/code/flaskbb/flaskbb.cfg]:
The name and port number of the exposed server.
If FlaskBB is accesible on port 80 you can just omit the port.
 For example, if FlaskBB is accessible via example.org:8080 than this is also what you would set here.
Server Name [example.org]: localhost:5000
Is HTTPS (recommended) or HTTP used for to serve FlaskBB?
Use HTTPS? [Y/n]: n
For Postgres use:
    postgresql://flaskbb@localhost:5432/flaskbb
For more options see the SQLAlchemy docs:
    http://docs.sqlalchemy.org/en/latest/core/engines.html
Database URI [sqlite:////Users/zhanghe/code/flaskbb/flaskbb.sqlite]: mysql+mysqldb://root:123456@127.0.0.1:3306/flaskbb?charset=utf8mb4
Redis will be used for things such as the task queue, caching and rate limiting.
Would you like to use redis? [Y/n]:
Redis URI [redis://localhost:6379]:
To use 'localhost' make sure that you have sendmail or
something similar installed. Gmail is also supprted.
Mail Server [localhost]:
The port on which the SMTP server is listening on.
Mail Server SMTP Port [25]:
If you are using a local SMTP server like sendmail this is not needed. For external servers it is required.
Use TLS for sending mails? [y/N]:
Same as above. TLS is the successor to SSL.
Use SSL for sending mails? [y/N]:
Not needed if you are using a local smtp server.
For gmail you have to put in your email address here.
Mail Username []:
Not needed if you are using a local smtp server.
For gmail you have to put in your gmail password here.
Mail Password []:
The name of the sender. You probably want to change it to something like '<your_community> Mailer'.
Mail Sender Name [FlaskBB Mailer]:
On localhost you want to use a noreply address here. Use your email address for gmail here.
Mail Sender Address [noreply@yourdomain]:
Logs and important system messages are sent to this address. Use your email address for gmail here.
Mail Admin Email [admin@yourdomain]:
Optional filepath to load a logging configuration file from. See the Python logging documentation for more detail.
	https://docs.python.org/library/logging.config.html#logging-config-fileformat
Logging Config Path []:
The configuration file has been saved to:
/Users/zhanghe/code/flaskbb/flaskbb.cfg
Feel free to adjust it as needed.
Usage:
flaskbb --config /Users/zhanghe/code/flaskbb/flaskbb.cfg run
```

安装
```
flaskbb install
```

```
(.venv) ➜  flaskbb git:(2.0.0) flaskbb install
[+] Installing FlaskBB...
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running stamp_revision  -> 5945d8081a95
[+] Creating default settings...
[+] Creating admin user...
Username [zhanghe]:
Email address: zhang_he06@163.com
Password: 123456
Repeat for confirmation: 123456
[+] Creating welcome forum...
[+] Installing default plugins...
[+] Compiling translations...
compiling catalog /Users/zhanghe/code/flaskbb/flaskbb/translations/pl/LC_MESSAGES/messages.po to /Users/zhanghe/code/flaskbb/flaskbb/translations/pl/LC_MESSAGES/messages.mo
compiling catalog /Users/zhanghe/code/flaskbb/flaskbb/translations/da/LC_MESSAGES/messages.po to /Users/zhanghe/code/flaskbb/flaskbb/translations/da/LC_MESSAGES/messages.mo
compiling catalog /Users/zhanghe/code/flaskbb/flaskbb/translations/sv_SE/LC_MESSAGES/messages.po to /Users/zhanghe/code/flaskbb/flaskbb/translations/sv_SE/LC_MESSAGES/messages.mo
compiling catalog /Users/zhanghe/code/flaskbb/flaskbb/translations/pt_BR/LC_MESSAGES/messages.po to /Users/zhanghe/code/flaskbb/flaskbb/translations/pt_BR/LC_MESSAGES/messages.mo
compiling catalog /Users/zhanghe/code/flaskbb/flaskbb/translations/zh_TW/LC_MESSAGES/messages.po to /Users/zhanghe/code/flaskbb/flaskbb/translations/zh_TW/LC_MESSAGES/messages.mo
compiling catalog /Users/zhanghe/code/flaskbb/flaskbb/translations/ru/LC_MESSAGES/messages.po to /Users/zhanghe/code/flaskbb/flaskbb/translations/ru/LC_MESSAGES/messages.mo
compiling catalog /Users/zhanghe/code/flaskbb/flaskbb/translations/zh_CN/LC_MESSAGES/messages.po to /Users/zhanghe/code/flaskbb/flaskbb/translations/zh_CN/LC_MESSAGES/messages.mo
compiling catalog /Users/zhanghe/code/flaskbb/flaskbb/translations/de/LC_MESSAGES/messages.po to /Users/zhanghe/code/flaskbb/flaskbb/translations/de/LC_MESSAGES/messages.mo
compiling catalog /Users/zhanghe/code/flaskbb/flaskbb/translations/fr/LC_MESSAGES/messages.po to /Users/zhanghe/code/flaskbb/flaskbb/translations/fr/LC_MESSAGES/messages.mo
compiling catalog /Users/zhanghe/code/flaskbb/flaskbb/translations/es/LC_MESSAGES/messages.po to /Users/zhanghe/code/flaskbb/flaskbb/translations/es/LC_MESSAGES/messages.mo
compiling catalog /Users/zhanghe/code/flaskbb/flaskbb/translations/en/LC_MESSAGES/messages.po to /Users/zhanghe/code/flaskbb/flaskbb/translations/en/LC_MESSAGES/messages.mo
[+] FlaskBB has been successfully installed!
```

启动
```
# 页面
flaskbb run
# 任务
flaskbb celery worker
```

[http://localhost:5000](http://localhost:5000)

登录
```
username: zhanghe
password: 123456
```

邮件
```
MAIL_SERVER = "smtp.163.com"
MAIL_PORT = 994
MAIL_USE_SSL = True
MAIL_USE_TLS = False
```
注意：为了维护良好的网络环境，自即日起阿里云新购服务器不再提供25端口邮件服务，建以尝试使用465加密端口发送邮件,或与邮件发信提供商咨询是否还有其他smtp发信端口

邮箱的安全协议（Gmail是TLS，qq和一些别的是SSL）

配置
```
# 安装插件
Management > Plugins > Portal > install
# 基础配置
Management > Settings > General Settings > 修改 Project subtitle & Project title
# 板块配置
Management > Forums > Add Category & Add Forum
```

部署
```
# 安装uwsgi
pip install uwsgi

# 安装supervisor
pip install supervisor

# 配置
mkdir etc
echo_supervisord_conf > etc/supervisord.conf
```

etc/supervisord.conf
```
[include]
files = *.ini
```

etc/flaskbb.ini
```
[uwsgi]
base = /var/apps/flaskbb
home = /var/apps/.virtualenvs/flaskbb/
pythonpath = %(base)
socket = 127.0.0.1:30002                    //与nginx通信的端口
module = wsgi
callable = flaskbb
uid = apps
gid = apps
logto = /var/apps/flaskbb/logs/uwsgi.log
plugins = python
```

nginx
```
server {
    listen 80;
    server_name forums.flaskbb.org;

    access_log /var/log/nginx/access.forums.flaskbb.log;
    error_log /var/log/nginx/error.forums.flaskbb.log;

    location / {
        try_files $uri @flaskbb;
    }

    # Static files
    location /static {
       alias /var/apps/flaskbb/flaskbb/static/;
    }

    location ~ ^/_themes/([^/]+)/(.*)$ {
        alias /var/apps/flaskbb/flaskbb/themes/$1/static/$2;
    }

    # robots.txt
    location /robots.txt {
        alias /var/apps/flaskbb/flaskbb/static/robots.txt;
    }

    location @flaskbb {
        uwsgi_pass 127.0.0.1:30002;
        include uwsgi_params;
    }
}
```
