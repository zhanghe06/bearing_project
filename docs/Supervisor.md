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
