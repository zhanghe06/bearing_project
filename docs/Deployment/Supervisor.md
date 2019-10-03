# Supervisor

http://www.supervisord.org

```bash
pip install supervisor
echo_supervisord_conf > etc/supervisord.conf
```

```bash
supervisorctl shutdown
supervisorctl status all
supervisorctl start all
supervisorctl stop all
supervisorctl restart all
supervisorctl reload
```

python中std.out与std.err

- 标准输出(std.out)
- 标准错误(std.err)

标准输出默认需要缓存后再输出到屏幕  
而标准错误则直接打印到屏幕

python2
```
python -u xxx.py
```
或者设置环境变量
```
export PYTHONUNBUFFERED=1
```
