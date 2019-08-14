# Flask-Babel

https://pythonhosted.org/Flask-Babel/

https://github.com/python-babel/flask-babel

http://babel.pocoo.org/en/latest/

安装
```bash
pip install Flask-Babel
```

查看本机支持的语言
```bash
pybabel --list-locales
```
注意：这里的简体中文是 zh_Hans_CN, 而不是 zh_CN

生成翻译模板
```bash
# pybabel extract -F babel.cfg -o messages.pot .
pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
```

修改翻译文件模板

首先记得将”messages.pot”中的”#, fuzzy”注释去掉，有这个注释在，将无法编译po文件。然后修改里面的项目信息内容如作者，版本等

删除`#, fuzzy`

创建中文翻译
```bash
pybabel init -i messages.pot -d translations -l zh_Hans_CN
```

修改翻译文件: translations/zh_Hans_CN/LC_MESSAGES/messages.po

编译翻译结果
```bash
pybabel compile -d translations
```

更新翻译
```bash
pybabel update -i messages.pot -d translations
```
